from tabulate import tabulate

from info_search.inverted_index_3.index import (
    load_inv_index_from_file,
    PageReader,
    Page,
)


def round_doc_vecs(doc_vecs: [{str: int}], max_signs: int):
    for vec in doc_vecs:
        for word, val in vec.items():
            if val > 0:
                vec[word] = round(vec[word], max_signs)


def calc_tf(
        docs: [Page],
        lexicon_volume: int,
        initial_doc_vec: {str: int},
        do_round: bool = True,
        max_signs: int = 5,
) -> [{str: int}]:

    tf_vecs = []
    for i, doc in enumerate(docs):
        doc_vec = initial_doc_vec.copy()
        for word in doc.words:
            try:
                doc_vec[word] += 1 / lexicon_volume
            except KeyError:
                print(f'No word {word}. Update inverted index')
        tf_vecs.append(doc_vec)

    if do_round:
        round_doc_vecs(tf_vecs, max_signs=max_signs)

    return tf_vecs


def stringify_vecs(doc_vecs: [{str: int}]) -> str:
    table_headers = list(doc_vecs[0].keys())
    rows = [vec.values() for vec in doc_vecs]
    return tabulate(rows, headers=table_headers, showindex=True)


def save_table(table: str, table_name: str) -> None:
    with open(table_name, 'w', encoding='utf-8') as f:
        f.write(table)


def run():
    inv_index = load_inv_index_from_file()
    docs = PageReader().parse_pages()
    lexicon_volume = len(inv_index)
    initial_doc_vec = {k: 0 for k in inv_index.keys()}

    tf_vecs = calc_tf(docs, lexicon_volume, initial_doc_vec)
    save_table(stringify_vecs(tf_vecs), 'tf.txt')


if __name__ == '__main__':
    run()
