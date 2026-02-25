from enum import Enum

GEMINI_TEMPERATURE = 0.8  # 0-2
MAX_TOKENS_TAILOR = 14000
MAX_TOKENS_ATS = 14000


class ValidFileExtensions(Enum):
    TEXT = ".txt"
    LATEX = ".tex"
    DOCX  = ".docx" 


class ValidKeyExtractorMethods(Enum):
    RANK_TF_IDF = "rank_tf_idf"
    GRAPH_BASED = "graph_based"
    LINGUISITC_SEMANTIC = "ling_semantic"
    KEYBERT = "keybert"
