import re
import json
from pathlib import Path
from typing import Type

from info_search.crawler_1.main import INDEX_NAME
from info_search.text_processing_2.main import PROCESSED_PAGES_FOLDER
from info_search.inverted_index_3.nodes import (
    fabricate_operator,
    Operand,
    Operator,
    LogicalNot,
    LogicalAnd,
    LogicalOr,
)


class IncorrectExpression(Exception):
    def __init__(self):
        message = 'Expression is incorrect'
        super().__init__(message)


class NoInvertedIndexFile(Exception):
    def __init__(self):
        message = 'File of inverted index was not found. Run main.py at first then try again.'
        super().__init__(message)


class Page:
    def __init__(self, i_str: str, url: str):
        self.words = []
        self.i_str = i_str
        self.url = url

    def __repr__(self):
        return f"{self.i_str} - {self.url}"

    def __len__(self):
        return len(self.words)


class InvertedIndex(dict):
    def lookup(self, expression: str):
        nodes = self.parse_expression(expression)
        answer = set()
        try:
            answer = sorted(self.reduce_nodes(nodes).docs)
        except IncorrectExpression as e:
            print(e)
        return answer

    def parse_expression(self, expression: str) -> [Operand | Operator]:
        tokens = expression.split()
        nodes = []
        for token in tokens:
            if token in ['!', 'НЕ', '&', 'И', '|', 'ИЛИ']:
                nodes.append(fabricate_operator(token))
            else:
                word = token.lower()
                try:
                    docs = self[word]
                except ValueError:
                    docs = set()
                nodes.append(Operand(docs, word))
        return nodes

    @staticmethod
    def contains_operator(
            nodes: [Operand | Operator],
            operator_type: Type[LogicalNot | LogicalAnd | LogicalOr],
    ) -> bool:
        for node in nodes:
            if isinstance(node, operator_type):
                return True
        return False

    def reduce_nodes(self, nodes: [Operand | Operator]) -> Operand:
        operators_precedence = [LogicalNot, LogicalAnd, LogicalOr]
        for operator in operators_precedence:
            while self.contains_operator(nodes, operator):
                for node in nodes:
                    if isinstance(node, operator):
                        operator_idx = nodes.index(node)
                        node.replace_with_new_operand(nodes, operator_idx)
                        break

        if not isinstance(nodes[0], Operand) or len(nodes) != 1:
            raise IncorrectExpression
        return nodes[0]


class PageReader:
    def __init__(self):
        self.pages: [Page] = []
        self.num_pages = 0

    def _read_index(self) -> None:
        index = Path('..', INDEX_NAME)
        with index.open(mode='r', encoding='utf-8') as f:
            for line in f:
                info = line.split()
                page_path = info[0]
                match = re.search(r"\d+", page_path)
                page_i = page_path[match.start():match.end()]
                self.pages.append(Page(page_i, info[1]))
                self.num_pages += 1

    @staticmethod
    def _preprocess_page(page: Page, text: str) -> None:
        text = text.replace(' . ', ' ')
        text.replace('!', '')
        text.replace('?', '')
        page.words = text.split()

    def _read_page(self, page: Page):
        page_path = Path('..', PROCESSED_PAGES_FOLDER, page.i_str + '.txt')
        with page_path.open('r', encoding='utf-8') as f:
            self._preprocess_page(page, f.read())

    def _read_pages(self):
        for page in self.pages:
            self._read_page(page)

    def parse_pages(self):
        self._read_index()
        self._read_pages()
        return self.pages


def make_index(pages: [Page]) -> InvertedIndex:
    inv_index = InvertedIndex()
    for i, page in enumerate(pages):
        for word in page.words:
            try:
                inv_index[word].add(i)
            except KeyError:
                inv_index[word] = {i}
    return inv_index


def sort_index(index: InvertedIndex):
    return InvertedIndex(sorted(index.items()))


def get_inv_index_path() -> Path:
    return Path('..', 'inverted_index.json')


def save_inv_index(index: InvertedIndex, rewrite: bool = False) -> None:
    inv_index_path = get_inv_index_path()
    if inv_index_path.exists() and not rewrite:
        return
    serializable_index = {key: list(values) for key, values in index.items()}
    with inv_index_path.open('w', encoding='utf-8') as f:
        json.dump(serializable_index, f, ensure_ascii=False, indent=4)


def load_inv_index_from_file() -> InvertedIndex:
    inv_index_path = get_inv_index_path()
    if not inv_index_path.exists():
        raise NoInvertedIndexFile
    with inv_index_path.open('r', encoding='utf-8') as f:
        inv_index = InvertedIndex(json.load(f))
    for key, values in inv_index.items():
        inv_index[key] = set(values)
    return inv_index
