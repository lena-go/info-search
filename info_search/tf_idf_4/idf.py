import csv
import math
from pathlib import Path

from info_search.inverted_index_3.index import InvertedIndex
from info_search.tf_idf_4.services import make_folder, TABLES_FOLDER_NAME


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
        make_folder(TABLES_FOLDER_NAME)
        filepath = Path('..', TABLES_FOLDER_NAME, 'idf.csv')
        with filepath.open('w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['term', 'idf'])
            for term in self.vec:
                row = [term, self.vec[term]]
                writer.writerow(row)
