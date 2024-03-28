import csv
import math

from info_search.inverted_index_3.index import InvertedIndex


class IDFVec:
    def __init__(self, total_docs: int = 100):
        self.vec = {}
        self.total_docs = total_docs

    def calc_for_corpus(
            self,
            inv_index: InvertedIndex,
            max_signs: int = 5,
            rewrite: bool = True,
    ) -> None:
        if self.vec and not rewrite:
            return
        self.vec = {}
        for word, doc_indices in inv_index.items():
            self.vec[word] = round(
                math.log(self.total_docs / len(doc_indices)),
                max_signs
            )

    def save_as_table(self):
        with open('idf.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['term', 'idf'])
            for term in self.vec:
                row = [term, self.vec[term]]
                writer.writerow(row)
