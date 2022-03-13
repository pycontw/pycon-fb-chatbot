from typing import List, Dict, Tuple

from recommendation_system.ranking_layer.base import BaseRankingModel

class SimpleRankingModel(BaseRankingModel):
    def __init__(self) -> None:
        super().__init__()

    def rank(self, user_features: Dict, candidates: List[List[Dict]]) -> List[Dict]:
        candidates = self.process_data(candidates=candidates)

        return candidates

    def process_data(self, candidates: List[List[Dict]]) -> List[List[Tuple]]:
        items_mapping = {}
        new_candidates = []

        for ranker in candidates:
            new_candidate_per_ranker = {}
            for i, candidate in enumerate(ranker):
                items_mapping.setdefault(candidate['title'], {
                    'title': candidates['title'],
                    'subtitle': candidates['subtitle'],
                    'image_url': candidates['image_url'],
                    'date': candidates['date'],
                    'url': candidates['url']
                })
                new_candidate_per_ranker[candidate['title']] = (i + 1, candidate['score']) # (rank, score)

            new_candidates.append(new_candidate_per_ranker)

        self._items_mapping = items_mapping

        return new_candidates
