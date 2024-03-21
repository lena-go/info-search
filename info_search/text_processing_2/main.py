import time
from pathlib import Path
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import string
import threading

import nltk
from nltk.corpus import stopwords
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)


INDEX_NAME = 'index.txt'
PROCESSED_PAGES_FOLDER = 'processed_pages'


def read_index() -> Queue:
    index = Path('..', INDEX_NAME)
    with index.open(encoding='utf-8') as f:
        files = Queue()
        for line in f:
            files.put(line.split()[0])
    return files


class PageProcessor:
    def __init__(self, processed_pages_path: Path):
        self.processed_pages_path = processed_pages_path
        self.lock = threading.Lock()

        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.morph_tagger = NewsMorphTagger(NewsEmbedding())

        self.punctuation = list(string.punctuation)
        self.punctuation.remove('-')
        self.punctuation.remove('.')
        self.punctuation += [' - ', '–', '—', '«', '»']

    def process_page(self, filename: str):
        page_path = Path('..', filename)
        with page_path.open(encoding='utf-8') as f:
            page = f.read()
        for symbol in self.punctuation:
            page = page.replace(symbol, ' ')

        doc = Doc(page)

        self.lock.acquire()
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)
        self.lock.release()

        lemmatized_text = ' '.join([
            token.lemma for token in doc.tokens
            if (token.lemma not in stopwords.words('russian') and token.lemma != '.')
        ])
        print(lemmatized_text)
        self.save_processed_page(filename.split('/')[1], lemmatized_text)

    def process_pages(self, files: Queue):
        while not files.empty():
            file_name = files.get()
            files.task_done()
            self.process_page(file_name)

    def save_processed_page(self, filename: str, text: str):
        path = self.processed_pages_path / filename
        with path.open(mode='w', encoding='utf-8') as f:
            f.write(text)
            f.write('\n')
        print(f"{path} was saved")


def make_folder(folder_path: Path):
    if not folder_path.is_dir():
        folder_path.mkdir()


def run():
    files = read_index()
    processed_pages_path = Path('..', PROCESSED_PAGES_FOLDER)
    make_folder(processed_pages_path)
    pp = PageProcessor(processed_pages_path)
    num_workers = 4
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for i in range(num_workers):
            executor.submit(pp.process_pages, files)


if __name__ == '__main__':
    nltk.download('stopwords')
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
