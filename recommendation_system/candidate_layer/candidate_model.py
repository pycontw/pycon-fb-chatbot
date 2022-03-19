

from typing import Dict, List
from recommendation_system.candidate_layer.base import BaseCandidateModel
from candidate_model_util import FastBM25


# demo data
from organic_data import user_features, article_data


# class BaseCandidateModel:
#     def __init__(self):
#         a = 0



class DemoCandidateModel(BaseCandidateModel):
    def __init__(self):
        super().__init__()
        # init simple article data data process
        self.document_list, self.title2organic = self.simple_article_data_process()
        title_list = list(self.title2organic.keys())

        # init BM25 model
        self.fast_bm25_model = FastBM25(corpus=self.document_list, title_list=title_list, batch_size=3)

        # init LM model


    def get_candidates(self, user_features: Dict) -> List[Dict]:
        tags = user_features['tags']
        query = ' '.join(tags)
        doc_element_with_score = self.fast_bm25_model.main(query=query)
        candidates = [self.title2organic[doc_element[0]] for doc_element in doc_element_with_score]
        return candidates


    def simple_article_data_process(self):
        document_list = []
        title2organic = dict()
        for article_data_element in article_data:
            data = article_data_element['title'] + ',' + article_data_element['subtitle']
            document_list.append(data)
            title2organic[article_data_element['title']] = article_data_element
        return document_list, title2organic







if __name__ == '__main__':
    print(DemoCandidateModel().get_candidates(user_features=user_features))