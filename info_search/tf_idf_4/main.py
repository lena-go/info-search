from tabulate import tabulate

from info_search.inverted_index_3.index import (
    load_inv_index_from_file,
    PageReader,
)


def run():
    inv_index = load_inv_index_from_file()
    initial_doc_vec = {k: 0 for k in inv_index.keys()}
    doc_vecs = []
    docs = PageReader().parse_pages()
    print(sorted(docs[0].words))
    lexicon_volume = len(inv_index)
    for i, doc in enumerate(docs):
        doc_vec = initial_doc_vec.copy()
        for word in doc.words:
            try:
                doc_vec[word] += 1 / lexicon_volume
            except KeyError:
                print(f'No word {word}. Update inverted index')
        doc_vecs.append(doc_vec)

    for vec in doc_vecs:
        for word, val in vec.items():
            if val > 0:
                vec[word] = round(vec[word], 5)

    table_headers = list(doc_vecs[0].keys())
    rows = [vec.values() for vec in doc_vecs]
    table = tabulate(rows, headers=table_headers, showindex=True)

    with open('table.txt', 'w', encoding='utf-8') as f:
        f.write(table)


if __name__ == '__main__':
    run()
