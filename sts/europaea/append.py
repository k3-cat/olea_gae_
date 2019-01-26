from .common import STATE_MAP, URL, PidLineCache, get_path, hyperlink
from .google_io import sheets


def fy(projs):
    path = get_path('KP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:K'
    path.row = f'{k}:{k+len(projs)}'
    rows = list()
    for proj in projs:
        rows.append([
            f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
            f'=HYPERLINK("{URL}/es?i={proj.pid},FY","[0000]")',
            hyperlink(proj['ids.doc'], 'FY'), ''
        ])
    sheets.append(path, rows)
    for row in rows:
        PidLineCache.append('FY', row[2][1:])
    return True

def kp(projs):
    path = get_path('KP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:K'
    path.row = f'{k}:{k+len(projs)}'
    rows = list()
    for i, proj in enumerate(projs, k):
        rows.append([
            f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
            f'=IF(D{i}="{STATE_MAP[5]}",HYPERLINK("{URL}/p?i={proj.pid},KP,","[跳过]"),"")',
            f'=HYPERLINK("{URL}/es?i={proj.pid},KP","[0000]")',
            hyperlink(proj['ids.doc'], 'GG'),
            f'=IF(E{i}="0/0","",createD(C{i}))'
        ])
    sheets.append(path, rows)
    for row in rows:
        PidLineCache.append('KP', row[2][1:])
    return True

def uj(proj):
    path = get_path('UJ')
    k = sheets.count_rows(path) + 1
    path.col = 'A:L'
    path.row = k
    row = [[
        f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
        f'=IF(D{k}="{STATE_MAP[5]}",HYPERLINK("{URL}/p?i={proj.pid},UJ,","[跳过]"),"")',
        f'=HYPERLINK("{URL}/es?i={proj.pid},UJ","[0000]")',
        hyperlink(proj['ids.doc'], 'GG'),
        hyperlink(proj['ids.ext'], 'KP'),
        f'=IF(E{k}="0/0","",createF(C{k}))'
    ]]
    sheets.append(path, row)
    PidLineCache.append('UJ', proj.pid)
    return True

def py(proj):
    path = get_path('PY')
    k = sheets.count_rows(path) + 1
    path.col = 'A:K'
    path.row = k
    row = [[
        f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
        f'=HYPERLINK("{URL}/es?i={proj.pid},PY","[0000]")',
        hyperlink(proj['ids.doc'], 'GG'),
        hyperlink(proj['ids.ext'], 'KP'),
        f'=IF(E{k}="0/0","",createF(C{k}))'
    ]]
    sheets.append(path, row)
    PidLineCache.append('PY', proj.pid)
    return True

def hq(proj):
    if proj['ssc'] in ('pu', 'hu'):
        if proj['req.UJ'] is None or proj['req.UJ'] == 0:
            pic_id = '{未知}'
        elif proj['ids.pic'] is not None:
            pic_id = '{绘制中}'
        else:
            pic_id = '{错误}'
    else:
        pic_id = proj['ids.pic']
    path = get_path('HQ')
    k = sheets.count_rows(path) + 1
    path.col = 'A:M'
    path.row = k
    row = [[
        f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
        f'=HYPERLINK("{URL}/es?i={proj.pid},HQ","[0000]")',
        hyperlink(proj['ids.doc'], 'GG'),
        hyperlink(proj['ids.ext'], 'KP'),
        hyperlink(proj['ids.mic'], 'PY'),
        hyperlink(pic_id, 'UJ'),
        f'=IF(E{k}="0/0","",createF(C{k}))'
    ]]
    sheets.append(path, row)
    PidLineCache.append('HQ', proj.pid)
    return True

def lb(proj_infos):
    path = get_path('LB')
    k = sheets.count_rows(path) + 1
    path.col = 'A:F'
    path.row = f'{k}:{k+len(proj_infos)}'
    rows = list()
    for pi in proj_infos:
        rows.append([f"'{pi[0]}", f"'{pi[1]}", f"'{pi[2]}", '初始', '', ''])
    sheets.append(path, rows)
    for row in rows:
        PidLineCache.append('LB', row[2][1:])
    return True

def up(proj):
    path = get_path('UP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:D'
    path.row = k
    row = [[f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}",
            f'=HYPERLINK("{URL}/p?i={proj.pid},UP","[設定鏈接]")']]
    sheets.append(path, row)
    PidLineCache.append('UP', proj.pid)
    return True
