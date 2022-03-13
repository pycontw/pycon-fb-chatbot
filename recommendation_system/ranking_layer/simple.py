from typing import List, Dict

from recommendation_system.ranking_layer.base import BaseRankingModel

class SimpleRankingModel(BaseRankingModel):
    def __init__(self) -> None:
        super().__init__()

    def rank(user_features: Dict, candidates: List[List[Dict]]) -> List[Dict]:

        return candidates
