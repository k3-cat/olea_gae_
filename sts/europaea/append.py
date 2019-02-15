from .cache import PidLineCache
from .common import get_path, hyperlink
from .global_value import STATE_MAP, URL
from .google_io import sheets


def fy(projs):
    path = get_path('FY')
    k = sheets.count_rows(path) + 1
    path.col = 'A:K'
    path.row = f'{k}:{k+len(projs)}'
    rows = list()
    for proj in projs:
        rows.append([
            f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}",
            STATE_MAP[5], '0/0', '', '',
            f'=HYPERLINK("{URL}/es?i={proj.pid},FY","[0000]")',
            hyperlink(proj['ids.doc'], 'FY'), ''
        ])
        PidLineCache.append('FY', proj.pid)
    sheets.append(path, rows)
    return True


def kp(projs):
    path = get_path('KP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:K'
    path.row = f'{k}:{k+len(projs)}'
    rows = list()
    for i, proj in enumerate(projs, k):
        rows.append([
            f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}",
            STATE_MAP[5], '0/0', '', '',
            f'=IF(D{i}="{STATE_MAP[5]}",HYPERLINK("{URL}/p?i={proj.pid},KP","[跳过]"),"")',
            f'=HYPERLINK("{URL}/es?i={proj.pid},KP","[0000]")',
            hyperlink(proj['ids.doc'], 'GG'), ''
        ])
        PidLineCache.append('KP', proj.pid)
    sheets.append(path, rows)
    return True


def uj(proj):
    path = get_path('UJ')
    k = sheets.count_rows(path) + 1
    path.col = 'A:L'
    path.row = k
    row = [[
        f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5],
        '0/0', '', '',
        f'=IF(D{k}="{STATE_MAP[5]}",HYPERLINK("{URL}/p?i={proj.pid},UJ","[跳过]"),"")',
        f'=HYPERLINK("{URL}/es?i={proj.pid},UJ","[0000]")',
        hyperlink(proj['ids.doc'], 'GG'),
        hyperlink(proj['ids.ext'], 'KP'), ''
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
        f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5],
        '0/0', '', '', f'=HYPERLINK("{URL}/es?i={proj.pid},PY","[0000]")',
        hyperlink(proj['ids.doc'], 'GG'),
        hyperlink(proj['ids.ext'], 'KP'), ''
    ]]
    sheets.append(path, row)
    PidLineCache.append('PY', proj.pid)
    return True


def hq(proj):
    if 'UJ' in proj['ssc']:
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
        f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", STATE_MAP[5],
        '0/0', '', '', f'=HYPERLINK("{URL}/es?i={proj.pid},HQ","[0000]")',
        hyperlink(proj['ids.doc'], 'GG'),
        hyperlink(proj['ids.ext'], 'KP'),
        hyperlink(proj['ids.mic'], 'PY'),
        hyperlink(pic_id, 'UJ'), ''
    ]]
    sheets.append(path, row)
    PidLineCache.append('HQ', proj.pid)
    return True


def lbcb(projs, sc):
    path = get_path(sc)
    k = sheets.count_rows(path) + 1
    path.col = 'A:F'
    path.row = f'{k}:{k+len(projs)}'
    rows = list()
    for proj in projs:
        rows.append([f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}", '初始', '', ''])
        PidLineCache.append(sc, proj.pid)
    sheets.append(path, rows)
    return True


def up(proj):
    path = get_path('UP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:D'
    path.row = k
    row = [[
        f"'{proj['ino']}", f"'{proj['title']}", f"'{proj.pid}",
        f'=HYPERLINK("{URL}/p?i={proj.pid},UP","[設定鏈接]")'
    ]]
    sheets.append(path, row)
    PidLineCache.append('UP', proj.pid)
    return True
