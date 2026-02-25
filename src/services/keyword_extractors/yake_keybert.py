import re
import math
import numpy as np
from collections import Counter

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

import yake
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.services.keyword_extractors import BaseKeywordsExtractor

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt_tab')

STOPWORDS = set(stopwords.words('english'))


class KeyBERTExtractor(BaseKeywordsExtractor):

    def __init__(
        self,
        embedding_model: str = 'all-MiniLM-L6-v2',
        diversity: float = 0.6,
        use_keybert_boost: bool = True
    ):
        """
        Args:
            embedding_model:    Any sentence-transformers model name.
                                Alternatives worth trying:
                                - 'paraphrase-mpnet-base-v2'  (slower, higher quality)
                                - 'all-mpnet-base-v2'         (best quality, slowest)
                                - 'all-MiniLM-L6-v2'          (fastest, good quality)
            diversity:          MMR diversity parameter (0.0–1.0).
                                0.4 for tight/focused lists, 0.7 for broad coverage.
            use_keybert_boost:  Whether to add KeyBERT candidates to the pool.
        """
        print(f"Loading embedding model: {embedding_model}...")
        self.st_model  = SentenceTransformer(embedding_model)
        self.kb_model  = KeyBERT(model=self.st_model) if use_keybert_boost else None
        self.diversity = diversity
        self.use_keybert_boost = use_keybert_boost
        print("Ready.")

    # ══════════════════════════════════════════════════════════════════════════════
    # STEP 1 — CANDIDATE GENERATION (YAKE + POS noun phrases)
    # ══════════════════════════════════════════════════════════════════════════════
    @staticmethod
    def yake_candidates(text: str, max_ngram: int = 3, top_n: int = 60) -> list[str]:
        """
        Use YAKE to extract a broad pool of statistical keyword candidates.
        We deliberately extract more than we need (top_n=60) since the semantic
        ranking step will filter and re-rank them.
        """
        extractor = yake.KeywordExtractor(
            lan="en",
            n=max_ngram,          # max phrase length
            dedupLim=0.8,         # dedup threshold (lower = more aggressive dedup)
            dedupFunc="seqm",     # sequence matcher for dedup
            windowsSize=2,        # co-occurrence window
            top=top_n,
            features=None
        )
        # YAKE returns (keyword, score) where LOWER score = more relevant
        keywords = extractor.extract_keywords(text)
        return [kw for kw, score in keywords]

    @staticmethod
    def pos_candidates(text: str) -> list[str]:
        """
        Extract noun-phrase candidates using POS tag patterns.
        Pattern: (JJ)* (NN|NNS|NNP|NNPS)+
        This ensures we're feeding the embedder meaningful technical phrases.
        """
        sentences = sent_tokenize(text)
        noun_tags = {'NN', 'NNS', 'NNP', 'NNPS'}
        adj_tags  = {'JJ', 'JJR', 'JJS'}
        valid_tags = noun_tags | adj_tags

        candidates = []
        for sent in sentences:
            tokens = word_tokenize(sent.lower())
            tagged = nltk.pos_tag(tokens)

            phrase = []
            for word, tag in tagged:
                if tag in valid_tags and word not in STOPWORDS and len(word) > 1:
                    phrase.append((word, tag))
                else:
                    if phrase:
                        # Only keep if phrase ends with a noun
                        if phrase[-1][1] in noun_tags:
                            candidates.append(' '.join(w for w, _ in phrase))
                        phrase = []
            # Flush remaining
            if phrase and phrase[-1][1] in noun_tags:
                candidates.append(' '.join(w for w, _ in phrase))

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for c in candidates:
            if c not in seen and len(c) > 2:
                seen.add(c)
                unique.append(c)
        return unique

    @staticmethod
    def get_candidates(text: str, max_ngram: int = 3, yake_top: int = 60) -> list[str]:
        """Merge YAKE and POS candidates into a single deduplicated pool."""
        yake_kw = KeyBERTExtractor.yake_candidates(text, max_ngram=max_ngram, top_n=yake_top)
        pos_kw  = KeyBERTExtractor.pos_candidates(text)

        seen = set()
        merged = []
        for kw in yake_kw + pos_kw:
            kw_clean = kw.strip().lower()
            if kw_clean not in seen and len(kw_clean) > 1:
                seen.add(kw_clean)
                merged.append(kw_clean)
        return merged


    # ══════════════════════════════════════════════════════════════════════════════
    # STEP 2 — SEMANTIC RANKING (EmbedRank cosine similarity)
    # ══════════════════════════════════════════════════════════════════════════════
    @staticmethod
    def embedrank(
        text: str,
        candidates: list[str],
        model: SentenceTransformer,
        top_n: int = 50
    ) -> list[tuple[str, float]]:
        """
        Embed the full document and all candidates, then rank candidates by
        cosine similarity to the document vector.
        Returns more than top_n so MMR has a larger pool to work with.
        """
        if not candidates:
            return []

        doc_embedding        = model.encode([text])                  # (1, dim)
        candidate_embeddings = model.encode(candidates)              # (n, dim)

        similarities = cosine_similarity(doc_embedding, candidate_embeddings)[0]  # (n,)

        ranked = sorted(
            zip(candidates, similarities, candidate_embeddings),
            key=lambda x: x[1],
            reverse=True
        )
        return [(kw, score, emb) for kw, score, emb in ranked[:top_n]]


    # ══════════════════════════════════════════════════════════════════════════════
    # STEP 3 — DEDUPLICATION via MMR (Maximal Marginal Relevance)
    # ══════════════════════════════════════════════════════════════════════════════
    @staticmethod
    def mmr(
        ranked_candidates: list[tuple[str, float, np.ndarray]],
        top_n: int = 30,
        diversity: float = 0.6
    ) -> list[tuple[str, float]]:
        """
        Maximal Marginal Relevance balances relevance vs diversity.
        
        diversity=0.0  → pure relevance (keywords may be redundant)
        diversity=1.0  → pure diversity (keywords may be off-topic)
        diversity=0.6  → good balance for ATS (recommended)

        At each step, picks the candidate that maximizes:
            MMR = (1 - diversity) * sim_to_doc - diversity * max_sim_to_selected
        """
        if not ranked_candidates:
            return []

        selected = []
        candidates = list(ranked_candidates)  # copy

        # Always pick the top-ranked candidate first
        best = candidates.pop(0)
        selected.append((best[0], best[1]))
        selected_embeddings = [best[2]]

        while len(selected) < top_n and candidates:
            mmr_scores = []
            for kw, doc_sim, emb in candidates:
                # Max similarity to any already-selected keyword
                sims_to_selected = cosine_similarity(
                    [emb], selected_embeddings
                )[0]
                max_sim_selected = max(sims_to_selected)

                score = (1 - diversity) * doc_sim - diversity * max_sim_selected
                mmr_scores.append((score, kw, doc_sim, emb))

            # Pick highest MMR score
            mmr_scores.sort(key=lambda x: x[0], reverse=True)
            _, best_kw, best_doc_sim, best_emb = mmr_scores[0]

            selected.append((best_kw, best_doc_sim))
            selected_embeddings.append(best_emb)

            # Remove selected from candidates
            candidates = [(kw, s, e) for kw, s, e in candidates if kw != best_kw]

        return selected


    # ══════════════════════════════════════════════════════════════════════════════
    # STEP 4 — OPTIONAL: KeyBERT pass for validation / extra candidates
    # ══════════════════════════════════════════════════════════════════════════════
    @staticmethod
    def keybert_candidates(
        text: str,
        kb_model: KeyBERT,
        top_n: int = 30,
        diversity: float = 0.6
    ) -> list[str]:
        """
        Run KeyBERT with MMR enabled as an additional candidate source.
        KeyBERT handles its own embedding + MMR internally.
        """
        keywords = kb_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 3),
            stop_words='english',
            use_mmr=True,
            diversity=diversity,
            top_n=top_n
        )
        return [kw for kw, _ in keywords]

    def extract(
        self,
        job_description: str,
        top_n: int = 30,
        yake_pool: int = 80,
        embedrank_pool: int = 60,
    ) -> list[tuple[str, float]]:
        """
        Full pipeline:
          1. YAKE + POS → candidate pool
          2. (optional) KeyBERT → additional candidates
          3. EmbedRank → semantic similarity ranking
          4. MMR → diverse, non-redundant final selection

        Args:
            job_description: Raw job description string.
            top_n:           Number of keywords to return.
            yake_pool:       How many YAKE candidates to generate.
            embedrank_pool:  How many top candidates to pass to MMR.

        Returns:
            List of (keyword, relevance_score) sorted by MMR selection order.
        """
        # Step 1 — Candidate generation
        print("Generating candidates (YAKE + POS)...")
        candidates = KeyBERTExtractor.get_candidates(job_description, yake_top=yake_pool)

        # Step 2 — KeyBERT boost (optional)
        if self.use_keybert_boost and self.kb_model:
            print("Running KeyBERT pass...")
            kb_kw = KeyBERTExtractor.keybert_candidates(job_description, self.kb_model, top_n=top_n)
            # Add KeyBERT candidates to pool if not already present
            existing = set(candidates)
            for kw in kb_kw:
                if kw not in existing:
                    candidates.append(kw)
                    existing.add(kw)

        print(f"Total candidate pool: {len(candidates)} phrases")

        # Step 3 — EmbedRank (semantic cosine similarity ranking)
        print("Running EmbedRank...")
        ranked = KeyBERTExtractor.embedrank(
            job_description,
            candidates,
            self.st_model,
            top_n=embedrank_pool
        )

        # Step 4 — MMR deduplication
        print("Applying MMR for diversity...")
        final = KeyBERTExtractor.mmr(ranked, top_n=top_n, diversity=self.diversity)

        return final

    def get_keywords(self, job_description: str, top_n: int = 30) -> list[str]:
        """Convenience method — returns just the keyword strings."""
        return [kw for kw, score in self.extract(job_description, top_n=top_n, yake_pool=(top_n*2))]
