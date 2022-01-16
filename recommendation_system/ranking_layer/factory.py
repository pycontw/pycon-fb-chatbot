from recommendation_system.ranking_layer.demo import DemoRankingModel
from recommendation_system.ranking_layer.base import BaseRankingModel
from typing import Text


class RankingFactory:
    @staticmethod
    def create(ranking_model_name: Text) -> BaseRankingModel:
        if ranking_model_name == "demo":
            return DemoRankingModel()
        raise NotImplementedError(
            f"Ranking model {ranking_model_name} is not implemented."
        )
