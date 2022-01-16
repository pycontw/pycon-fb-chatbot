from recommendation_system.candidate_layer.demo import DemoCandidateModel
from recommendation_system.candidate_layer.base import BaseCandidateModel
from typing import Text


class CandidateFactory:
    @staticmethod
    def create(candidate_model_name: Text) -> BaseCandidateModel:
        if candidate_model_name == "demo":
            return DemoCandidateModel()
        raise NotImplementedError(
            f"Candidate model {candidate_model_name} is not implemented."
        )
