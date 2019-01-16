from .append import lb
from .database import Project


def proj(items):
    rows = list()
    projs = list()
    for item_ in items:
        if ';' not in item_:
            continue
        item = item_.split(';')
        if item[2] == '':
            if item[0] != '':
                item[2] = f'scp-{item[0]}'
        projs.append(Project(pid=None, info=(item[0], item[1], item[2])))
        rows.append([f"'{item[0]}", f"'{item[1]}", f"'{projs[-1].pid}"])
    lb(rows)
    return projs
