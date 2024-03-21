from index import PageReader, make_index, sort_index, save_inv_index


def run():
    reader = PageReader()
    pages = reader.parse_pages()
    inv_index_unsorted = make_index(pages)
    inv_index = sort_index(inv_index_unsorted)
    # save_inv_index(inv_index)
    # print(inv_index)

    print(inv_index.lookup('противительный & ! противиться | противник'))


if __name__ == '__main__':
    run()

"""
 'противительный': {16, 18, 22, 15}
 'противиться': {16, 18}
 'противник': {15}
"""