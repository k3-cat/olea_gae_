from . import sheets
from .common import SC2D_MAP, STATE_MAP, PidLineCache, get_path, hyperlink


HL_COL_MAP = {
    'KP': 'K',
    'PY': 'K',
    'UJ': 'L',
    'HQ': 'M'}

def set_hyperlink(pid, sc, id_):
    path = get_path(sc)
    path.col = HL_COL_MAP[sc]
    path.row = PidLineCache.get(sc, pid)
    sheets.set_values(path, [[hyperlink(id_, sc)]])
    return True

def update_m_process_info(proj):
    path = get_path('LB')
    path.col = 'D:E'
    path.row = PidLineCache.get('LB', proj.pid)
    list_name = proj['staff'].list_staff(sc_range=['FY', 'KP', 'PY', 'UJ', 'HQ'])
    staff_display = list()
    for sc in list_name:
        if not list_name[sc][0] and not list_name[sc][1]:
            continue
        staff_display.append(f'{SC2D_MAP[sc]}: {", ".join(list_name[sc][0]+list_name[sc][1])}')
    sheets.set_values(path, [[proj.ssc_display, ' | '.join(staff_display)]])
    return True

def update_s_state(proj, sc):
    if sc == 'UP':
        return 'SKIP'
    path = get_path(sc)
    path.col = 'D:G'
    path.row = PidLineCache.get(sc, proj.pid)
    part_list_name = proj['staff'].list_staff(sc_range=[sc])[sc]
    if sc in proj['staff']:
        count = f"'{len(proj[f'staff.{sc}'])}/{proj[f'req.{sc}']}"
    else:
        count = '0/0'
    sheets.set_values(path, [[
        STATE_MAP[proj['staff'].get_state(sc)],
        count,
        ', '.join(part_list_name[0]),
        ', '.join(part_list_name[1])]])
    return True
