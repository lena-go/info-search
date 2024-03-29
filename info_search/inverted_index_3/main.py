from index import (
    PageReader,
    InvertedIndex,
    make_index,
    sort_index,
    save_inv_index,
    load_inv_index_from_file
)


def get_inv_index(rewrite_index: bool = False) -> InvertedIndex:
    inv_index = None
    if not rewrite_index:
        try:
            inv_index = load_inv_index_from_file()
        except FileNotFoundError:
            pass
    if not inv_index:
        reader = PageReader()
        pages = reader.parse_pages()
        inv_index_unsorted = make_index(pages)
        inv_index = sort_index(inv_index_unsorted)
        save_inv_index(inv_index, rewrite_index)
    return inv_index


def run(rewrite_index: bool = False):
    inv_index = get_inv_index(rewrite_index)
    # while True:
    # print('Enter your query:')
    # query = input()
    query = 'противительный ИЛИ видеться ИЛИ видимо'
    results = inv_index.lookup(query)
    print(results)


if __name__ == '__main__':
    run(rewrite_index=False)

"""
Examples:
 противительный: 15, 16, 18, 22
 противник: 15
 видимо: 16, 18, 29, 57, 96
 видеться: 88
 
 противительный И противник ИЛИ видимо
 противительный ИЛИ противник ИЛИ видимо
 противительный И противник И видимо
 противительный И НЕ противник ИЛИ НЕ видимо
 противительный ИЛИ НЕ противник ИЛИ НЕ видимо
"""
