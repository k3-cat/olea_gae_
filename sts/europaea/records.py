import time

from . import sheets
from .common import STATE_MAP, get_path, hyperlink


HL_COL_MAP = {
    'KP': 'K',
    'UJ': 'K',
    'PY': 'K',
    'HQ': 'L'}

def set_hyperlink(sc, pos, id_):
    path = get_path(sc)
    path.col = HL_COL_MAP[sc]
    path.row = pos
    sheets.set_values(path, [[hyperlink(id_, sc)]])
    return True

class LbLineCache:
    cache = dict()
    time = 0

    @classmethod
    def update(cls):
        now = time.time()
        if now - cls.time < 120:
            return
        cls.cache.clear()
        path = get_path('LB')
        path.col = 'C'
        path.row = '2:'
        for k, line in enumerate(sheets.get_values(path), 2):
            if not line:
                continue
            cls.cache[line[0]] = k

def get_LB_line(pid):
    LbLineCache.update()
    return LbLineCache.cache[pid]

def update_process_info(proj):
    path = get_path('LB')
    path.col = 'D:E'
    path.row = get_LB_line(proj.pid)
    sheets.set_values(path, [[proj.ssc_display, proj['staff'].list_staff()]])
    return True

def update_state(proj, sc, pos):
    path = get_path(sc)
    path.col = 'D'
    path.row = pos
    state = STATE_MAP[proj['staff'].get_state(sc)]
    sheets.set_values(path, [[state]])
    return True

def update_req_display(proj, sc, pos):
    path = get_path(sc)
    path.col = 'E'
    path.row = pos
    req_display = f'{len(proj[f"staff.{sc}"])}/{proj[f"req.{sc}"]}'
    sheets.set_values(path, [[req_display]])
    return True

def update_nickname_display(proj, sc, pos):
    path = get_path(sc)
    path.row = pos
    path.col = 'F'
    sheets.set_values(path, [[proj['staff'].list_staff(sc_range=[sc], finished=True)]])
    path.col = 'G'
    sheets.set_values(path, [[proj['staff'].list_staff(sc_range=[sc], finished=False)]])
    path_ = get_path('LB')
    path_.row = get_LB_line(proj.pid)
    path_.col = 'E'
    sheets.set_values(path_, [[proj['staff'].list_staff()]])
    return True
