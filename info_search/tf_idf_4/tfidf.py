from info_search.tf_idf_4.services import save_list_as_table


class TFIDFVecs:
    def __init__(self, tf_vecs: [{str: int}], idf_vec: {str: int}):
        self.tf_vecs = tf_vecs
        self.idf_vec = idf_vec
        self.tfidf_vecs = []

    def calc(self, rewrite: bool = True, max_signs: int = 5) -> None:
        if self.tfidf_vecs and not rewrite:
            return
        self.tfidf_vecs = []
        for tf_vec in self.tf_vecs:
            tfidf_vec = {}
            for term, tf in tf_vec.items():
                tfidf_vec[term] = round(tf * self.idf_vec[term], max_signs)
            self.tfidf_vecs.append(tfidf_vec)

    def save_as_table(self):
        save_list_as_table(self.tfidf_vecs, 'tfidf.csv')
