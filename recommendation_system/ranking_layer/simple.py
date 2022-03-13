from copy import deepcopy
from typing import List, Dict, Tuple

from recommendation_system.ranking_layer.base import BaseRankingModel

class SimpleRankingModel(BaseRankingModel):
    def __init__(self) -> None:
        super().__init__()

    def rank(self, user_features: Dict, candidates: List[List[Dict]]) -> List[Dict]:
        candidates = self.process_data(candidates=candidates)
        rankings = self.calc_candidate_score(candidates=candidates)

        new_candidates = []
        for item, score in rankings:
            new_item = self.get_item(item)
            new_item['score'] = score
            new_candidates.append(new_item)

        return new_candidates[:3]

    def get_item(self, item):
        return deepcopy(self._items_mapping[item])

    def calc_candidate_score(self, candidates):
        candidate_ranking = {}

        for item in self._items_mapping:
            candidate_ranking.setdefault(item, [])
            for ranker in candidates:
                if item in ranker:
                    k, score = ranker.get(item)
                    candidate_ranking[item].append(score/k)

        for item, scores in candidate_ranking.items():
            candidate_ranking[item] = sum(scores)

        return sorted(candidate_ranking.items(), key=lambda d: d[1], reverse=True)

    def process_data(self, candidates: List[List[Dict]]) -> List[List[Tuple]]:
        items_mapping = {}
        new_candidates = []

        for ranker in candidates:
            new_candidate_per_ranker = {}
            for i, candidate in enumerate(ranker):
                items_mapping.setdefault(candidate['title'], {
                    'title': candidate['title'],
                    'subtitle': candidate['subtitle'],
                    'image_url': candidate['image_url'],
                    'date': candidate['date'],
                    'url': candidate['url']
                })
                new_candidate_per_ranker[candidate['title']] = (i + 1, candidate.get('score')) # (rank, score)

            new_candidates.append(new_candidate_per_ranker)

        self._items_mapping = items_mapping

        return new_candidates
