import time

from info_search.inverted_index_3.index import (
    load_inv_index_from_file,
    PageReader,
)
from info_search.tf_idf_4.tf import TFVec
from info_search.tf_idf_4.idf import IDFVec
from info_search.tf_idf_4.tfidf import TFIDFVec
from info_search.tf_idf_4.services import save_serialized


def calc_vecs_for_corpus() -> (TFVec, IDFVec, TFIDFVec):
    inv_index = load_inv_index_from_file()
    docs = PageReader().parse_pages()

    tf_vecs = TFVec(inv_index)
    tf_vecs.calc_for_corpus(docs)

    idf_vec = IDFVec()
    idf_vec.calc_for_corpus(inv_index)

    tfidf_vecs = TFIDFVec(tf_vecs.vecs, idf_vec.vec)
    tfidf_vecs.calc_for_corpus()

    return tf_vecs, idf_vec, tfidf_vecs


def run():
    tf, idf, tfidf = calc_vecs_for_corpus()
    tf.save_as_table()
    idf.save_as_table()
    tfidf.save_as_table()
    save_serialized(tf, 'tf.pickle')
    save_serialized(idf, 'idf.pickle')
    save_serialized(tfidf, 'tfidf.pickle')


if __name__ == '__main__':
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
