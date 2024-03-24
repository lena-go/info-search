import csv

from info_search.inverted_index_3.index import Page, InvertedIndex


class TFVec:
    def __init__(self):
        self.vecs = []

    def round_tf_vecs(self, max_signs: int):
        for vec in self.vecs:
            for word, val in vec.items():
                if val > 0:
                    vec[word] = round(vec[word], max_signs)

    def calc_tf(
            self,
            docs: [Page],
            lexicon_volume: int,
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
            for word in doc.words:
                try:
                    doc_vec[word] += 1 / lexicon_volume
                except KeyError:
                    print(f'No word {word}. Update inverted index')
            self.vecs.append(doc_vec)
        if do_round:
            self.round_tf_vecs(max_signs=max_signs)

    def save_as_table(self):
        with open('tf.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            total_docs = len(self.vecs)
            writer.writerow(['term'] + list(range(total_docs)))
            for term in self.vecs[0]:
                row = [term] + [self.vecs[i][term] for i in range(total_docs)]
                writer.writerow(row)
