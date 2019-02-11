from . import append, auto_title
from .cache import PageCache
from .database import Project


def projects(items, type_):
    rows = list()
    projs = list()
    errors = list()
    for item_ in items:
        if ';' not in item_:
            continue
        item = item_.split(';')
        item[0] = item[0].upper()
        if item[1] == '':
            if item[0] != '':
                item[1] = auto_title.fetch_title_by_item_no(item[0])
            elif item[1] != '':
                item[1] = auto_title.fetch_title_by_url(item[1])
            else:
                item[1] = '[E]'
            if '[E]' in item[1]:
                errors.append(item[0], None, item[2], item[1])
                continue
        pid = Project.find_pid(item[1])
        if pid:
            errors.append(item[0], item[1], item[2], f'exist: {pid}')
            continue
        if item[2] == '':
            if item[0] != '':
                item[2] = f'scp-{item[0]}'
            else:
                errors.append(None, item[1], None, 'miss url')
                continue
        projs.append(Project.create_proj(item[0], item[1], item[2]))
        rows.append([item[0], item[1], projs[-1].pid])
    PageCache.clear_cache()
    append.lb(rows)
    if type_ == 'T':
        append.fy(projs)
    elif type_ in ('G', 'K'):
        append.kp(projs)
    return errors
