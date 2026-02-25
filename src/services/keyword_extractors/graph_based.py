import networkx as nx
from collections import Counter, defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

from src.services.keyword_extractors import BaseKeywordsExtractor

nltk.download('wordnet')

STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


class GraphBasedExtractor(BaseKeywordsExtractor):

    # ── RAKE ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def _preprocess(text: str) -> list[str]:
        tokens = word_tokenize(text.lower())
        return [
            lemmatizer.lemmatize(t) for t in tokens
            if t.isalpha() and t not in STOPWORDS and len(t) > 2
        ]


    # ── TextRank ──────────────────────────────────────────────────────────────────
    @staticmethod
    def textrank_keywords(text: str, window: int = 4, top_n: int = 30) -> list[tuple[str, float]]:
        """Classic TextRank on a word co-occurrence graph."""
        tokens = GraphBasedExtractor._preprocess(text)

        graph = nx.Graph()
        graph.add_nodes_from(set(tokens))

        for i, word in enumerate(tokens):
            for j in range(i + 1, min(i + window, len(tokens))):
                neighbor = tokens[j]
                if graph.has_edge(word, neighbor):
                    graph[word][neighbor]['weight'] += 1
                else:
                    graph.add_edge(word, neighbor, weight=1)

        scores = nx.pagerank(graph, weight='weight')
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


    # ── Co-occurrence Graph with Betweenness Centrality ───────────────────────────
    @staticmethod
    def cooccurrence_centrality_keywords(text: str, window: int = 5, top_n: int = 30) -> list[tuple[str, float]]:
        """Words that bridge concepts (high betweenness = key connector terms)."""
        tokens = GraphBasedExtractor._preprocess(text)
        graph = nx.Graph()
        
        for i, word in enumerate(tokens):
            for j in range(i + 1, min(i + window, len(tokens))):
                neighbor = tokens[j]
                if graph.has_edge(word, neighbor):
                    graph[word][neighbor]['weight'] += 1
                else:
                    graph.add_edge(word, neighbor, weight=1)

        # Betweenness centrality: words that connect different topic clusters
        centrality = nx.betweenness_centrality(graph, weight='weight', normalized=True)
        return sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]


    # ── PositionRank (position-biased TextRank) ───────────────────────────────────
    @staticmethod
    def positionrank_keywords(text: str, window: int = 4, top_n: int = 30) -> list[tuple[str, float]]:
        """
        Words appearing earlier (requirements, title) get higher prior weight.
        Mimics the PositionRank paper heuristic.
        """
        tokens = GraphBasedExtractor._preprocess(text)

        # Position prior: earlier = higher weight
        position_prior = defaultdict(float)
        for i, token in enumerate(tokens):
            position_prior[token] += 1.0 / (i + 1)

        # Normalize
        total = sum(position_prior.values())
        personalization = {w: v / total for w, v in position_prior.items()}

        graph = nx.Graph()
        graph.add_nodes_from(set(tokens))
        for i, word in enumerate(tokens):
            for j in range(i + 1, min(i + window, len(tokens))):
                neighbor = tokens[j]
                if graph.has_edge(word, neighbor):
                    graph[word][neighbor]['weight'] += 1
                else:
                    graph.add_edge(word, neighbor, weight=1)

        scores = nx.pagerank(graph, weight='weight', personalization=personalization)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_keywords(self, job_description: str, top_n: int = 30) -> list[str]:
        tr_kw   = {kw for kw, _ in GraphBasedExtractor.textrank_keywords(job_description, top_n=top_n)}
        cc_kw   = {kw for kw, _ in GraphBasedExtractor.cooccurrence_centrality_keywords(job_description, top_n=top_n)}
        pr_kw   = {kw for kw, _ in GraphBasedExtractor.positionrank_keywords(job_description, top_n=top_n)}

        vote = Counter()
        for kw in tr_kw: vote[kw] += 2
        for kw in cc_kw: vote[kw] += 2
        for kw in pr_kw: vote[kw] += 3  # Position-biased = most ATS-relevant

        return sorted(vote.keys(), key=lambda k: vote[k], reverse=True)[:top_n]