import pymorphy2

from info_search.tf_idf_4.tf import TFVec
from info_search.tf_idf_4.idf import IDFVec
from info_search.tf_idf_4.tfidf import TFIDFVec
from info_search.inverted_index_3.index import InvertedIndex
from info_search.search_engine_5.services import (
    calc_vector_len,
    calc_cos_similarity,
)


class RelevantDoc:
    def __init__(self, idx: int):
        self.idx = idx
        self.weight = 0

    def __repr__(self):
        return f"{self.idx:<4} {self.weight}"


class SearchEngine:
    def __init__(
            self,
            corpus_tf: TFVec,
            corpus_idf: IDFVec,
            corpus_tfidf: TFIDFVec,
            inv_index: InvertedIndex,
    ):
        self.corpus_tf = corpus_tf
        self.corpus_idf = corpus_idf
        self.corpus_tfidf = corpus_tfidf
        self.inv_index = inv_index
        self.morph = pymorphy2.MorphAnalyzer()

    def preprocess_query(self, query: str) -> [str]:
        lemmas = []
        for word in query.lower().split():
            lemmas.append(
                self.morph.parse(word)[0].normal_form
            )
        return lemmas

    @staticmethod
    def print_query_vec(vec: {str: float}, step: str = None) -> None:
        if step:
            print(step)
        for term, val in vec.items():
            if val > 0:
                print(term, val)

    def calc_query_vec(self, lemmas: [str], print_meta: bool = False) -> {str: float}:
        query_vec = self.corpus_tf.calc(lemmas)
        if print_meta:
            self.print_query_vec(query_vec, 'tf')
        for term in lemmas:
            query_vec[term] *= self.corpus_idf.vec[term]
        if print_meta:
            self.print_query_vec(query_vec, 'tf-idf')
        return query_vec

    def update_weights(self, query_vec: {str: float}, docs: [RelevantDoc]) -> None:
        query_vec_len = calc_vector_len(query_vec)
        for doc in docs:
            doc.weight = calc_cos_similarity(
                query_vec,
                self.corpus_tfidf.tfidf_vecs[doc.idx],
                query_vec_len,
            )

    def get_relevant_docs(self, query_vec: {str: float}, query_lemmas: [str]) -> [RelevantDoc]:
        relevant_doc_indices = set()
        for term in query_lemmas:
            relevant_doc_indices.update(self.inv_index[term])
        relevant_docs = [RelevantDoc(i) for i in relevant_doc_indices]
        self.update_weights(query_vec, relevant_docs)
        return sorted(relevant_docs, key=lambda doc: doc.weight, reverse=True)

    def search(self, query: str, print_meta: bool = False) -> [RelevantDoc]:
        all_query_lemmas = self.preprocess_query(query)
        query_lemmas = []
        for term in all_query_lemmas:
            if term in self.inv_index:
                query_lemmas.append(term)
        query_vec = self.calc_query_vec(query_lemmas, print_meta)
        search_results = self.get_relevant_docs(query_vec, query_lemmas)
        return search_results
