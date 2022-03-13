import pytest

import mock

from recommendation_system.main import RecommendationSystem


class MockCandidateModel:
    def __init__(self, candidate_model_name):
        del candidate_model_name
        self.candidate_id = 0

    def get_candidates(self, features):
        del features
        candidates = [{"title": f"title {self.candidate_id}"}]
        self.candidate_id += 1
        return candidates


class MockRankingModel:
    def __init__(self, ranking_model_name):
        del ranking_model_name

    def rank(self, candidates):
        return candidates


def test_RecommendationSystem_recommend_one_candidate_model_one_ranking_model(
    monkeypatch,
):
    monkeypatch.setattr(
        "recommendation_system.candidate_layer.factory.CandidateFactory.create",
        MockCandidateModel,
    )
    monkeypatch.setattr(
        "recommendation_system.ranking_layer.factory.RankingFactory.create",
        MockRankingModel,
    )
    RecommendationSystem._load_experiment_config = staticmethod(
        lambda v: {"candidate_models": ["1"], "ranking_model": "a"}
    )

    recipient_id = "1234"

    assert RecommendationSystem.recommend(recipient_id=recipient_id) == [
        {"title": "title 0"}
    ]


def test_RecommendationSystem_recommend_two_candidate_models_one_ranking_model(
    monkeypatch,
):
    monkeypatch.setattr(
        "recommendation_system.candidate_layer.factory.CandidateFactory.create",
        MockCandidateModel,
    )
    monkeypatch.setattr(
        "recommendation_system.ranking_layer.factory.RankingFactory.create",
        MockRankingModel,
    )
    RecommendationSystem._load_experiment_config = staticmethod(
        lambda v: {"candidate_models": ["1", "2"], "ranking_model": "a"}
    )

    recipient_id = "1234"

    assert RecommendationSystem.recommend(recipient_id=recipient_id) == [
        {"title": "title 0"},
        {"title": "title 0"},
    ]
