import csv
import pickle
from pathlib import Path


TABLES_FOLDER_NAME = 'vec_tables'
CORPUS_VECS_FOLDER_NAME = 'corpus_vecs'


def save_list_as_table(vecs: [{str: int}], filename: str) -> None:
    make_folder(TABLES_FOLDER_NAME)
    filepath = Path('..', TABLES_FOLDER_NAME, filename)
    with filepath.open('w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        total_docs = len(vecs)
        writer.writerow(['term'] + list(range(total_docs)))
        for term in vecs[0]:
            row = [term] + [vecs[i][term] for i in range(total_docs)]
            writer.writerow(row)


def make_folder(folder_name: str) -> None:
    folder = Path('..', folder_name)
    if not folder.is_dir():
        folder.mkdir()


def save_serialized(obj, filename: str) -> None:
    make_folder(CORPUS_VECS_FOLDER_NAME)
    filepath = Path('..', CORPUS_VECS_FOLDER_NAME, filename)
    with filepath.open('wb') as f:
        pickle.dump(obj, f)


def load_serialized(filename: str):
    filepath = Path('..', CORPUS_VECS_FOLDER_NAME, filename)
    with filepath.open('rb') as f:
        obj = pickle.load(f)
    return obj
