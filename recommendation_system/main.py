from typing import Text, List, Dict
from recommendation_system.candidate_layer.factory import CandidateFactory
from recommendation_system.ranking_layer.factory import RankingFactory


class RecommendationSystem(object):
    @classmethod
    def recommend(cls, recipient_id: Text) -> List[Dict]:
        """
        main logic is as follow:
        1. get experiment config
        2. get feature
        3. use candidate layer to get candidates
        4. use ranking layer to sort candidates
        5. filter out some posts or items according to compliance
        6. return the result
        """
        experiment_config: Dict = cls._load_experiment_config(recipient_id)
        user_features: Dict = cls._get_feature(recipient_id)
        candidates: List[List[Dict]] = []
        for cancidate_model in cls._get_candidate_models(experiment_config):
            candidates.append(cancidate_model.get_candidates(user_features))
        # TODO: For now, it only support 1 ranking layer. We should suuport multiple ranking layers to sort at some point.
        result = cls._get_ranking_model(experiment_config).rank(user_features, candidates)
        filtered_result = cls._filter(result)
        return filtered_result

    @staticmethod
    def _load_experiment_config(recipient_id):
        """
        TODO: just an example, we should load experiment config from database
        """
        return {
            "candidate_models": [
                "demo",
                # 'other candidate model for you guys to implement'
            ],
            "ranking_model": "simple",
            # TODO: should replace base ranking model with your own!
        }

    @staticmethod
    def _get_feature(recipient_id: Text) -> Dict:
        """
        TODO: Get the user's features from the database, by issuing a query to BigQuery or Postgres

        """
        # this is just a placeholder
        return {
            "demographic": {
                "age": 20,
                "gender": "M",
                "city": "Taipei",
                "career": "Software Engineer",
            },
            "is_volunteer": True,
            "python_experience": 4,
            "tags": ["youtube", "ML"],
            "vectors": [0, 0, 0],
        }

    @staticmethod
    def _get_candidate_models(experiment_config: Dict):
        """
        TODO: should only return candidate models specified in experiment_config
        """
        return [
            CandidateFactory.create(candidate_model_name=candidate_model_name)
            for candidate_model_name in experiment_config["candidate_models"]
        ]

    @staticmethod
    def _get_ranking_model(experiment_config: Dict):
        # TODO: For now, it only return 1 ranking model. We should implement multiple ranking models to sort at some point.
        ranking_model_name = experiment_config["ranking_model"]
        return RankingFactory.create(ranking_model_name=ranking_model_name)

    @staticmethod
    def _filter(result: List[Dict]) -> List[Dict]:
        """
        TODO: implement business-logic related filtering here
        e.g. If a company didn't sponsor PyConTW, then we should remove all of their posts from the result
        """
        filtered_result = result
        return filtered_result


if __name__ == "__main__":
    result = RecommendationSystem.recommend(recipient_id="1413683625375061")
    print(result)
