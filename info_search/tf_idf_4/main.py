import time

from info_search.inverted_index_3.index import (
    load_inv_index_from_file,
    PageReader,
)
from info_search.tf_idf_4.tf import TFVec
from info_search.tf_idf_4.idf import IDFVec
from info_search.tf_idf_4.tfidf import TFIDFVec


def run():
    inv_index = load_inv_index_from_file()
    docs = PageReader().parse_pages()

    tf_vecs = TFVec()
    tf_vecs.calc(docs, inv_index)
    tf_vecs.save_as_table()

    idf_vec = IDFVec()
    idf_vec.calc(inv_index)
    idf_vec.save_as_table()

    tfidf_vecs = TFIDFVec(tf_vecs.vecs, idf_vec.vec)
    tfidf_vecs.calc()
    tfidf_vecs.save_as_table()


if __name__ == '__main__':
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
