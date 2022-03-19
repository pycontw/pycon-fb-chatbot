import abc
from typing import Dict, List


class BaseRankingModel(abc.ABC):
    @abc.abstractmethod
    def rank(user_features: Dict, candidates: List[List[Dict]]) -> List[Dict]:
        pass
