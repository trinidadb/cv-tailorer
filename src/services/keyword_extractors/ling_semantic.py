import re
import math
from collections import Counter, defaultdict
from itertools import combinations

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from src.services.keyword_extractors import BaseKeywordsExtractor

STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Domain-specific tech/HR terms to boost (expand for your domain)
DOMAIN_BOOST_TERMS = {
    'python', 'java', 'sql', 'aws', 'machine learning', 'deep learning',
    'agile', 'scrum', 'docker', 'kubernetes', 'ci/cd', 'rest', 'api',
    'data analysis', 'communication', 'leadership', 'teamwork',
    'problem solving', 'bachelor', 'master', 'degree', 'experience',
    'bachelor\'s', 'master\'s', 'years', 'required', 'preferred',
    'react', 'node', 'cloud', 'devops', 'spark', 'tensorflow', 'pytorch',
}


class SemanticExtractor(BaseKeywordsExtractor):
    # ── POS Pattern Mining ────────────────────────────────────────────────────────
    @staticmethod
    def pos_pattern_keywords(text: str, top_n: int = 30) -> list[tuple[str, int]]:
        """
        Extract phrases matching ATS-relevant POS patterns:
        - (JJ)* NN+        → 'senior software engineer'
        - NN IN NN         → 'experience with python'
        - VBG NN+          → 'building scalable systems'
        """
        sentences = sent_tokenize(text)
        candidates = []
        
        patterns = [
            # Adjective(s) + Noun(s)
            r'(JJ[RS]?\s)*(NN[PS]?\s)*NN[PS]?',
            # Noun + preposition + Noun
            r'NN[PS]?\sIN\sNN[PS]?',
            # Gerund + Noun
            r'VBG\sNN[PS]?',
        ]

        for sent in sentences:
            tokens = word_tokenize(sent.lower())
            tagged = nltk.pos_tag(tokens)
            
            # Build tag string for regex matching
            tag_str = ' '.join(tag for _, tag in tagged)
            word_list = [word for word, _ in tagged]
            
            for pattern in patterns:
                for match in re.finditer(pattern, tag_str):
                    # Map character positions to token indices
                    start_tag_idx = tag_str[:match.start()].count(' ')
                    end_tag_idx = tag_str[:match.end()].count(' ')
                    phrase_words = word_list[start_tag_idx:end_tag_idx + 1]
                    phrase = ' '.join(
                        w for w in phrase_words if w not in STOPWORDS and len(w) > 1
                    )
                    if phrase and len(phrase.split()) >= 1:
                        candidates.append(phrase)

        freq = Counter(candidates)
        return freq.most_common(top_n)


    # ── PMI (Pointwise Mutual Information) for Bigrams ───────────────────────────
    @staticmethod
    def pmi_keywords(text: str, top_n: int = 30, min_freq: int = 1) -> list[tuple[str, float]]:
        """
        High PMI bigrams are strongly collocated — signal real skill/requirement phrases.
        PMI(x,y) = log[ P(x,y) / (P(x) * P(y)) ]
        """
        tokens = [
            t.lower() for t in word_tokenize(text)
            if t.isalpha() and t.lower() not in STOPWORDS and len(t) > 2
        ]

        unigram_freq = Counter(tokens)
        bigram_freq = Counter(zip(tokens, tokens[1:]))
        total_unigrams = sum(unigram_freq.values())
        total_bigrams = sum(bigram_freq.values())

        pmi_scores = {}
        for (w1, w2), count in bigram_freq.items():
            if count < min_freq:
                continue
            p_xy = count / total_bigrams
            p_x = unigram_freq[w1] / total_unigrams
            p_y = unigram_freq[w2] / total_unigrams
            if p_x * p_y > 0:
                pmi = math.log2(p_xy / (p_x * p_y))
                pmi_scores[f"{w1} {w2}"] = pmi

        return sorted(pmi_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


    # ── Domain-Boosted Frequency Scoring ─────────────────────────────────────────
    @staticmethod
    def domain_boosted_keywords(text: str, top_n: int = 30, boost: float = 3.0) -> list[tuple[str, float]]:
        """
        Count all unigrams + bigrams, then multiply by `boost` if they're domain terms.
        Simple but highly tunable for specific industries.
        """
        text_lower = text.lower()
        tokens = [
            t for t in word_tokenize(text_lower)
            if t.isalpha() and t not in STOPWORDS and len(t) > 2
        ]

        freq: dict[str, float] = Counter(tokens)
        bigrams = [f"{a} {b}" for a, b in zip(tokens, tokens[1:])]
        for bg in bigrams:
            freq[bg] = freq.get(bg, 0) + 1

        # Apply domain boost
        for term in list(freq.keys()):
            if term in DOMAIN_BOOST_TERMS:
                freq[term] *= boost

        return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]


    def get_keywords(self, job_description: str, top_n: int = 30) -> list[str]:
        pos_kw    = {kw for kw, _ in SemanticExtractor.pos_pattern_keywords(job_description, top_n)}
        pmi_kw    = {kw for kw, _ in SemanticExtractor.pmi_keywords(job_description, top_n)}
        domain_kw = {kw for kw, _ in SemanticExtractor.domain_boosted_keywords(job_description, top_n)}

        vote = Counter()
        for kw in pos_kw:    vote[kw] += 2
        for kw in pmi_kw:    vote[kw] += 2
        for kw in domain_kw: vote[kw] += 3  # Domain awareness = highest ATS weight

        return sorted(vote.keys(), key=lambda k: vote[k], reverse=True)[:top_n]