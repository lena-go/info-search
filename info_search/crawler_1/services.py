from pathlib import Path

from info_search.crawler_1.main import (
    PAGES_FOLDER,
    NUM_PAGES,
)


def remove_blanks_from_pages():
    folder_path = Path('..', PAGES_FOLDER)
    for i in range(NUM_PAGES):
        filename = folder_path / (str(i) + '.txt')
        with filename.open('r', encoding='utf=8') as f:
            data = f.read()
        while '\n\n' in data:
            data = data.replace('\n\n', '\n')
        with filename.open('w', encoding='utf-8') as f:
            f.write(data)


if __name__ == '__main__':
    remove_blanks_from_pages()
