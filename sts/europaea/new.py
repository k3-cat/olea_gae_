from .common import sheets, get_path
from .database import Project


def proj(inos, titles, doc_urls):
    path = get_path('LB')
    k = sheets.count_rows(path) + 1
    path.col = 'A:C'
    path.row = f'{k}:{k+len(titles)}'
    rows = list()
    projs = list()
    for ino, title, doc_url in zip(inos, titles, doc_urls):
        projs.append(Project(pid=None, info=(ino, title, doc_url)))
        rows.append([f"'{ino}", f"'{title}", f"'{projs[-1].pid}"])
    sheets.append(path, rows)
    return projs
