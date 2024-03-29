from math import sqrt


def calc_dot_product(vec1: {str: float}, vec2: {str: float}) -> float:
    result = 0
    for term in vec1:
        result += vec1[term] * vec2[term]
    return result


def calc_vector_len(vec: {str: float}) -> float:
    sm = 0
    for val in vec.values():
        sm += val * val
    return sqrt(sm)


def calc_cos_similarity(vec1: {str: float}, vec2: {str: float}, len1: float = None) -> float:
    dot_product = calc_dot_product(vec1, vec2)
    if not len1:
        len1 = calc_vector_len(vec1)
    len2 = calc_vector_len(vec2)
    return dot_product / (len1 * len2)

