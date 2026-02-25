from abc import ABC, abstractmethod


class BaseKeywordsExtractor(ABC):

    @abstractmethod
    def get_keywords(self, job_description: str, top_n: int = 30):
        pass
