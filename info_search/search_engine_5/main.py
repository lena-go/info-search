import time

from info_search.tf_idf_4.main import calc_vecs_for_corpus
from info_search.tf_idf_4.services import load_serialized
from info_search.inverted_index_3.index import load_inv_index_from_file
from info_search.search_engine_5.search_engine import SearchEngine


def run():
    try:
        tf = load_serialized('tf.pickle')
        idf = load_serialized('idf.pickle')
        tfidf = load_serialized('tfidf.pickle')
    except FileNotFoundError:
        tf, idf, tfidf = calc_vecs_for_corpus()

    inv_index = load_inv_index_from_file()
    search_engine = SearchEngine(tf, idf, tfidf, inv_index)

    while True:
        user_query = input()
        search_engine.search(user_query)


if __name__ == '__main__':
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
