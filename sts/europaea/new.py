from .append import lb, fy, kp
from .database import Project
from .auto_title import fetch_title


def projects(items, type_):
    rows = list()
    projs = list()
    errors = list()
    for item_ in items:
        if ';' not in item_:
            continue
        item = item_.split(';')
        if item[1] == '':
            item[1] = fetch_title(item[0])
            if '[E]' in item[1]:
                errors.append(item[0], None, item[2], item[1])
                continue
        pid = Project.find_pid(item[1])
        if pid:
            errors.append(item[0], item[1], item[2], pid)
            continue
        if item[2] == '':
            if item[0] != '':
                item[2] = f'scp-{item[0]}'
        projs.append(Project(pid=None, info=(item[0], item[1], item[2])))
        rows.append([item[0], item[1], projs[-1].pid])
    lb(rows)
    if type_ == 'T':
        fy(projs)
    elif type_ in ('G', 'K'):
        kp(projs)
    return errors
