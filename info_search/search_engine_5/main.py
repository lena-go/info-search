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
        print('Enter your query:')
        user_query = input()
        results = search_engine.search(user_query, print_meta=False)
        if not results:
            print('Sorry, nothing was found :(')
            continue
        print(f'{len(results)} documents at all')
        for doc in results:
            print(doc)


if __name__ == '__main__':
    run()

"""
Input examples:
    запятая
    запятая союз
    запятая союз подчинительные
"""
