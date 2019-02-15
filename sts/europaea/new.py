from . import append, auto_title
from .cache import PageCache
from .database import Project


def check(func):
    def wrapper(lines):
        items = list()
        for line in lines:
            if line.count(';') != 2:
                continue
            items.append(line.split(';'))
        func(items, list(), list())
    return wrapper


@check
def fill_G(items, errs, valids):
    for item in items:
        if not item[1]:
            if item[0]:
                item[1] = auto_title.fetch_title_by_item_no(item[0])
            elif item[2]:
                item[1] = auto_title.fetch_title_by_url(item[2])
            else:
                item[1] = '[E] empty'
        if '[E]' in item[1]:
            errs.append(('G', item[0], None, item[2], item[1]))
            continue
        if not item[2]:
            if item[0]:
                item[2] = f'scp-{item[0]}'
            else:
                errs.append(('G', None, item[1], None, '[E] miss url'))
        valids.append(item)
    return errs, valids


@check
def fill_C(items, errs, valids):
    for item in items:
        if not item[1]:
            errs.append(('C', None, item[1], None, '[E] miss title'))
            continue
        valids.append(item)
    return errs, valids


@check
def fill_K(items, errs, valids):
    for item in items:
        if not item[1]:
            errs.append(('K', None, item[1], None, '[E] miss title'))
            continue
        if not item[2]:
            errs.append(('K', None, item[1], None, '[E] miss doc url'))
            continue
        valids.append(item)
    return errs, valids


FILL_MAP = {'K': fill_K, 'C': fill_C, 'T': fill_G, 'G': fill_G}


def projects(items, type_):
    rows = list()
    projs = list()
    errs, valids = FILL_MAP[type_](items, type_)
    for item in valids:
        pid = Project.find_pid(item[1])
        if pid:
            errs.append((item[0], item[1], item[2], f'[E] exist: {pid}'))
            continue
        projs.append(Project.create_proj(item[0], item[1], item[2]))
        rows.append((item[0], item[1], projs[-1].pid))
    PageCache.clear_cache()
    if type_ == 'T':
        append.lbcb(rows, sc='LB')
        append.fy(projs)
    elif type_ in ('G', 'K'):
        append.lbcb(rows, sc='LB')
        append.kp(projs)
    elif type_ == 'C':
        append.lbcb(rows, sc='CB')
    return errs
