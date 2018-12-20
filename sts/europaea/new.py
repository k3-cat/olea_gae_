from . import sheet, get_path
from .database import Project


def new_proj(inos, titles, doc_urls):
    path = get_path('LB')
    k = sheet.count_rows(path) + 1
    path.col = 'A:C'
    path.row = f'k:{k+len(titles)}'
    rows = list()
    projs = list()
    for ino, title, doc_url in zip(inos, titles, doc_urls):
        projs.append(Project(pid=None, info=(ino, title, doc_url)))
        rows.append([[ino, title, projs[-1].pid]])
    sheet.append(path, rows)
    return projs
