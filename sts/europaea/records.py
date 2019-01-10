import time

from . import sheets
from .common import SC2D_MAP, STATE_MAP, get_path, hyperlink


HL_COL_MAP = {
    'KP': 'K',
    'PY': 'K',
    'UJ': 'L',
    'HQ': 'M'}

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

def update_m_process_info(proj):
    path = get_path('LB')
    path.col = 'D:E'
    path.row = get_LB_line(proj.pid)
    list_name = proj['staff'].list_staff()
    staff_display = list()
    for sc in list_name:
        if not list_name[sc][0] and not list_name[sc][1]:
            continue
        staff_display.append(f'{SC2D_MAP[sc]}: {", ".join(list_name[sc][0]+list_name[sc][1])}')
    sheets.set_values(path, [[proj.ssc_display, ' | '.join(staff_display)]])
    return True

def update_s_state(proj, sc, pos):
    path = get_path(sc)
    path.col = 'D:G'
    path.row = pos
    part_list_name = proj['staff'].list_staff(sc_range=[sc])[sc]
    sheets.set_values(path, [[
        STATE_MAP[proj['staff'].get_state(sc)],
        f'{len(proj[f"staff.{sc}"])}/{proj[f"req.{sc}"]}',
        ', '.join(part_list_name[0]),
        ', '.join(part_list_name[1])]])
    return True
