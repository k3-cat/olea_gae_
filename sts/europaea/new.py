from .common import sheets, get_path
from .database import Project


def proj(datas):
    path = get_path('LB')
    k = sheets.count_rows(path) + 1
    path.col = 'A:C'
    data = datas.split('|')
    path.row = f'{k}:{k+len(data)}'
    rows = list()
    projs = list()
    for item_ in data:
        item = item_.split(';')
        projs.append(Project(pid=None, info=(item[0], item[1], item[2])))
        rows.append([f"'{item[0]}", f"'{item[1]}", f"'{projs[-1].pid}", '初始'])
    sheets.append(path, rows)
    return projs
