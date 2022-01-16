from recommendation_system.ranking_layer.base import BaseRankingModel
from typing import List, Dict


class DemoRankingModel(BaseRankingModel):
    def __init__(self):
        super().__init__()

    def rank(self, candidates: List[Dict]) -> List[Dict]:
        return candidates
