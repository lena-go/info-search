NUM_PAGES = 100


class NoMatchingOperator(Exception):
    def __init__(self, sign):
        message = f"Matching operator for {sign} wasn't found"
        super().__init__(message)


class Operand:
    def __init__(self, docs: {int}, word: str = None):
        self.docs = docs
        self.word = word

    def __neg__(self):
        all_docs = {i for i in range(NUM_PAGES)}
        return all_docs - self.docs

    def __and__(self, other: 'Operand'):
        return self.docs & other.docs

    def __or__(self, other: 'Operand'):
        return self.docs | other.docs

    def __repr__(self):
        if self.word:
            return f"({self.word})"
        return "(no_name)"


class Operator:
    def __init__(self):
        pass


class UnaryOperator(Operator):
    def __init__(self):
        super().__init__()


class LogicalNot(UnaryOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def replace_with_new_operand(nodes: [Operand, Operator], operator_idx: int):
        next_node = nodes[operator_idx + 1]
        # all_docs = {i for i in range(NUM_PAGES)}
        del nodes[operator_idx: operator_idx + 2]
        # merged_node = Operand(all_docs - next_node.docs)
        merged_node = Operand(-next_node)
        nodes.insert(operator_idx, merged_node)

    def __repr__(self):
        return '!'


class BinaryOperator(Operator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def pop_old_nodes(
            nodes: [Operand, Operator],
            operator_idx: int
    ) -> (Operand, Operand):
        prev_node = nodes[operator_idx - 1]
        next_node = nodes[operator_idx + 1]
        del nodes[operator_idx-1: operator_idx+2]
        return prev_node, next_node


class LogicalAnd(BinaryOperator):
    def __init__(self):
        super().__init__()

    def replace_with_new_operand(self, nodes: [Operand, Operator], operator_idx: int):
        prev_node, next_node = self.pop_old_nodes(nodes, operator_idx)
        merged_node = Operand(prev_node & next_node)
        nodes.insert(operator_idx - 1, merged_node)

    def __repr__(self):
        return '&'


class LogicalOr(BinaryOperator):
    def __init__(self):
        super().__init__()

    def replace_with_new_operand(self, nodes: [Operand, Operator], operator_idx: int):
        prev_node, next_node = self.pop_old_nodes(nodes, operator_idx)
        merged_node = Operand(prev_node | next_node)
        nodes.insert(operator_idx - 1, merged_node)

    def __repr__(self):
        return '|'


def fabricate_operator(sign: str) -> Operator:
    if sign in ['!', 'НЕ']:
        return LogicalNot()
    if sign in ['&', 'И']:
        return LogicalAnd()
    if sign in ['|', 'ИЛИ']:
        return LogicalOr()
    raise NoMatchingOperator
