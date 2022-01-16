import abc
from typing import Dict, List


class BaseCandidateModel(abc.ABC):
    @abc.abstractmethod
    def get_candidates(user_features: Dict) -> List[Dict]:
        pass
