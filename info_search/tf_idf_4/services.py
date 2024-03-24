import csv


def save_list_as_table(vecs: [{str: int}], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        total_docs = len(vecs)
        writer.writerow(['term'] + list(range(total_docs)))
        for term in vecs[0]:
            row = [term] + [vecs[i][term] for i in range(total_docs)]
            writer.writerow(row)
