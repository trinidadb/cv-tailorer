import re
import math
from collections import Counter, defaultdict
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer

from src.services.keyword_extractors import BaseKeywordsExtractor

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt_tab')

STOPWORDS = set(stopwords.words('english'))


class RakeTFIDFExtractor(BaseKeywordsExtractor):

    # ── RAKE ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def rake_keywords(text: str, top_n: int = 30) -> list[tuple[str, float]]:
        """Rapid Automatic Keyword Extraction."""
        # Split into candidate phrases on stopwords / punctuation
        splitters = STOPWORDS | set(string.punctuation)
        word_pattern = re.compile(r'[a-zA-Z+#\-]+')

        sentences = sent_tokenize(text.lower())
        phrases = []
        for sent in sentences:
            words = word_pattern.findall(sent)
            phrase = []
            for w in words:
                if w in splitters:
                    if phrase:
                        phrases.append(phrase)
                        phrase = []
                else:
                    phrase.append(w)
            if phrase:
                phrases.append(phrase)

        # Word frequency and degree
        word_freq = Counter()
        word_degree = defaultdict(int)
        for phrase in phrases:
            for w in phrase:
                word_freq[w] += 1
                word_degree[w] += len(phrase) - 1

        # Score = degree / frequency
        word_score = {w: (word_degree[w] + word_freq[w]) / word_freq[w] for w in word_freq}

        phrase_scores = {}
        for phrase in phrases:
            score = sum(word_score[w] for w in phrase)
            phrase_scores[' '.join(phrase)] = score

        return sorted(phrase_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


    # ── TF-IDF (single-document, uses sub-sentences as "documents") ───────────────
    @staticmethod
    def tfidf_keywords(text: str, top_n: int = 30) -> list[tuple[str, float]]:
        """TF-IDF treating each sentence as a document."""
        sentences = sent_tokenize(text)
        if len(sentences) < 2:
            sentences = text.split('.')

        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            max_features=500,
            token_pattern=r'[a-zA-Z+#\-]{2,}'
        )
        tfidf_matrix = vectorizer.fit_transform(sentences)
        scores = tfidf_matrix.sum(axis=0).A1
        vocab = vectorizer.get_feature_names_out()

        keyword_scores = sorted(zip(vocab, scores), key=lambda x: x[1], reverse=True)
        return keyword_scores[:top_n]


    # ── Noun Chunk Frequency ───────────────────────────────────────────────────────
    @staticmethod
    def noun_chunk_keywords(text: str, top_n: int = 30) -> list[tuple[str, int]]:
        """Extract frequent noun phrases using POS tagging (no spaCy needed)."""
        tokens = word_tokenize(text.lower())
        tagged = nltk.pos_tag(tokens)

        # Grammar: optional adjective(s) followed by one or more nouns
        noun_phrase_tags = {'NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS'}
        noun_tags = {'NN', 'NNS', 'NNP', 'NNPS'}

        phrases = []
        i = 0
        while i < len(tagged):
            word, tag = tagged[i]
            if tag in noun_phrase_tags and word not in STOPWORDS and len(word) > 2:
                phrase = [word]
                j = i + 1
                while j < len(tagged) and tagged[j][1] in noun_phrase_tags and tagged[j][0] not in STOPWORDS:
                    phrase.append(tagged[j][0])
                    j += 1
                # Only keep if it ends in a noun
                if tagged[j-1][1] in noun_tags if j > i+1 else tag in noun_tags:
                    phrases.append(' '.join(phrase))
                i = j
            else:
                i += 1

        freq = Counter(phrases)
        return freq.most_common(top_n)

    def get_keywords(self, job_description: str, top_n: int = 30) -> list[str]:
        """Combine RAKE + TF-IDF + Noun Chunks, deduplicate, return top keywords."""
        rake_kw  = {kw for kw, _ in RakeTFIDFExtractor.rake_keywords(job_description, top_n)}
        tfidf_kw = {kw for kw, _ in RakeTFIDFExtractor.tfidf_keywords(job_description, top_n)}
        noun_kw  = {kw for kw, _ in RakeTFIDFExtractor.noun_chunk_keywords(job_description, top_n)}

        # Union with priority weighting via vote count
        vote = Counter()
        for kw in rake_kw:  vote[kw] += 3   # RAKE scores multi-word well
        for kw in tfidf_kw: vote[kw] += 2
        for kw in noun_kw:  vote[kw] += 1

        ranked = sorted(vote.keys(), key=lambda k: vote[k], reverse=True)
        return ranked[:top_n]