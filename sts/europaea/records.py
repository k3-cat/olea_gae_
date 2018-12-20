from .GoogleIO import sheet
from . import get_path, hyperlink


def set_hyperlink(sc, row, id_):
    path = get_path(sc)
    if sc == 'PY':
        path.col = 'K'
    elif sc == 'KP':
        path.col = 'L'
    elif sc in ('HQ', 'MS'):
        path.col = 'J'
    path.row = row
    sheet.set_values(path, [[hyperlink(id_, sc)]])
    return True

def get_LB_line(pid):
    return Cache.title.cache(pid)[3]

def update_process_info(proj):
    path = get_path('LB')
    path.col = 'B:C'
    path.row = get_LB_line(proj.pid)
    sheet.set_values(path, [[proj.ssc_display, proj.all_staff]])
    return True
