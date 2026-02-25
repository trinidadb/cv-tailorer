# WIP - poor performance
import os
from src.config.constants import ValidKeyExtractorMethods
from src.services.keyword_extractors.base import BaseKeywordsExtractor

def get_extractors():
    extractors = {}

    is_enabled = os.getenv("MULTIPLE_KEYWORD_EXTRACTORS", "false").lower() == "true"

    if is_enabled:
        from src.services.keyword_extractors.rake_tf_idf import RakeTFIDFExtractor
        from src.services.keyword_extractors.graph_based import GraphBasedExtractor
        from src.services.keyword_extractors.ling_semantic import SemanticExtractor
        from src.services.keyword_extractors.yake_keybert import KeyBERTExtractor
        extractors[ValidKeyExtractorMethods.RANK_TF_IDF] = RakeTFIDFExtractor
        extractors[ValidKeyExtractorMethods.GRAPH_BASED] = GraphBasedExtractor
        extractors[ValidKeyExtractorMethods.LINGUISITC_SEMANTIC] = SemanticExtractor
        extractors[ValidKeyExtractorMethods.KEYBERT] = KeyBERTExtractor

    return extractors