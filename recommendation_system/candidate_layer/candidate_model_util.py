




from gensim.summarization.bm25 import BM25





class FastBM25:
    def __init__(self, corpus=list, title_list=list, batch_size=32):
        # init
        self.title_list = title_list
        
        # word segmentation
        self.corpus_ws = self.word_segmentation(corpus=corpus, batch_size=batch_size)
        
        # lauch bm25 moidel
        self.bm25 = BM25(self.corpus_ws)


    def word_segmentation(self, corpus=list ,batch_size=int):
        # init parameter and container
        corpus_ws = []
        batch_num = int(len(corpus) / batch_size) + 1
        # main
        for i in range(batch_num):
            batch_corpus = corpus[i*batch_size : (i+1)*batch_size]
            batch_corpus_ws = self.word_segmentation_func(batch_corpus=batch_corpus)
            corpus_ws += batch_corpus_ws
        return corpus_ws
    
    def word_segmentation_func(self, batch_corpus=list):
        batch_corpus_ws = batch_corpus
        batch_corpus_ws = [sent.split() for sent in batch_corpus]
        return batch_corpus_ws
    
    
    def main(self, query=str):
        query_ws = self.word_segmentation_func(batch_corpus=[query])[0]
        scores = self.bm25.get_scores(query_ws)
        #xprint(self.corpus_ws)
        element_with_score = [[self.title_list[i], sent_ws, scores[i]] for i, sent_ws in enumerate(self.corpus_ws)]
        element_with_score = sorted(element_with_score, reverse=True, key=lambda x:x[2])
        return element_with_score



