from collections import Counter

from info_search.inverted_index_3.index import Page, InvertedIndex
from info_search.tf_idf_4.services import save_list_as_table


class TFVec:
    def __init__(self):
        self.vecs = []

    def round_tf_vecs(self, max_signs: int):
        for vec in self.vecs:
            for word, val in vec.items():
                if val > 0:
                    vec[word] = round(vec[word], max_signs)

    def calc(
            self,
            docs: [Page],
            inv_index: InvertedIndex,
            do_round: bool = True,
            max_signs: int = 5,
            rewrite: bool = True,
    ) -> None:
        if self.vecs and not rewrite:
            return
        self.vecs = []
        initial_doc_vec = {k: 0 for k in inv_index.keys()}
        for i, doc in enumerate(docs):
            doc_vec = initial_doc_vec.copy()
            token_counts = Counter(doc.words)
            for term, freq in token_counts.items():
                try:
                    doc_vec[term] = freq / len(doc)
                except KeyError:
                    print(f'No word {term}. Update inverted index')
            self.vecs.append(doc_vec)
        if do_round:
            self.round_tf_vecs(max_signs=max_signs)

    def save_as_table(self) -> None:
        save_list_as_table(self.vecs, 'tf.csv')
