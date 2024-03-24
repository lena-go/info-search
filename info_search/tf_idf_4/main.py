import time

from info_search.inverted_index_3.index import (
    load_inv_index_from_file,
    PageReader,
)
from info_search.tf_idf_4.tf import TFVec
from info_search.tf_idf_4.idf import IDFVec


def run():
    inv_index = load_inv_index_from_file()
    docs = PageReader().parse_pages()
    lexicon_volume = len(inv_index)

    tf_vecs = TFVec()
    tf_vecs.calc_tf(docs, lexicon_volume, inv_index)
    tf_vecs.save_as_table()

    idf_vec = IDFVec()
    idf_vec.calc_idf(inv_index)
    idf_vec.save_as_table()


if __name__ == '__main__':
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
