from src.config.constants import ValidKeyExtractorMethods
from src.services.keyword_extractors import get_extractors


class KeywordsExtractor:

    @staticmethod
    def get(job_description: str, method: ValidKeyExtractorMethods, top_n: int = 30):
        extractors = get_extractors()
        match method:
            case ValidKeyExtractorMethods.RANK_TF_IDF:
                try:
                    RakeTFIDFExtractor = extractors[ValidKeyExtractorMethods.RANK_TF_IDF]
                    return RakeTFIDFExtractor().get_keywords(job_description, top_n=top_n)
                except Exception as e:
                    raise

            case ValidKeyExtractorMethods.GRAPH_BASED:
                try:
                    GraphBasedExtractor = extractors[ValidKeyExtractorMethods.GRAPH_BASED]
                    return GraphBasedExtractor().get_keywords(job_description, top_n=top_n)
                except Exception as e:
                    raise

            case ValidKeyExtractorMethods.LINGUISITC_SEMANTIC:
                try:
                    SemanticExtractor = extractors[ValidKeyExtractorMethods.LINGUISITC_SEMANTIC]
                    return SemanticExtractor().get_keywords(job_description, top_n=top_n)
                except Exception as e:
                    raise

            case ValidKeyExtractorMethods.KEYBERT:
                try:
                    KeyBERTExtractor = extractors[ValidKeyExtractorMethods.KEYBERT]
                    return KeyBERTExtractor().get_keywords(job_description, top_n=top_n)
                except Exception as e:
                    raise

