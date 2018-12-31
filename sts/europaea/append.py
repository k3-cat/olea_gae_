from .google_io import sheets
from .common import get_path, hyperlink, STATE_MAP, URL


def fy(projs):
    path = get_path('KP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:K'
    path.row = f'{k}:{k+len(projs)}'
    rows = list()
    for proj in projs:
        rows.append([
            f"'{proj.ino}", f"'{proj.title}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
            f'=HYPERLINK("{URL}/p?p={proj.pid}&s=FY&r="&ROW(),"[人员]")',
            hyperlink(proj.urls['doc'], 'FY'), ''
        ])
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
            f"'{proj.ino}", f"'{proj.title}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
            f'=IF(D11={STATE_MAP[5]},"",HYPERLINK("{URL}/p?p={proj.pid}&s=KP&r="&ROW(),"[跳过]"))',
            f'=HYPERLINK("{URL}/p?p={proj.pid}&s=KP&r="&ROW(),"[人员]")',
            hyperlink(proj.urls['doc'], 'GG'),
            f'=IF(D{i}="0/0","",createD(C{i},ROW()))'
        ])
    sheets.append(path, rows)
    return True

def sj(proj):
    path = get_path('SJ')
    k = sheets.count_rows(path) + 1
    path.col = 'A:L'
    path.row = k
    row = [[
        f"'{proj.ino}", f"'{proj.title}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
        f'=IF(D11={STATE_MAP[5]},"",HYPERLINK("{URL}/p?p={proj.pid}&s=SJ&r="&ROW(),"[跳过]"))',
        f'=HYPERLINK("{URL}/p?p={proj.pid}&s=SJ&r="&ROW(),"[人员]")',
        hyperlink(proj.urls['doc'], 'GG'),
        hyperlink(proj.urls['ext'], 'KP'),
        f'=IF(E{k}="0/0","",createF(C{k},ROW()))'
    ]]
    sheets.append(path, row)
    return True

def py(proj):
    path = get_path('PY')
    k = sheets.count_rows(path) + 1
    path.col = 'A:K'
    path.row = k
    row = [[
        f"'{proj.ino}", f"'{proj.title}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
        f'=HYPERLINK("{URL}/p?p={proj.pid}&s=PY&r="&ROW(),"[人员]")',
        hyperlink(proj.urls['doc'], 'GG'),
        hyperlink(proj.urls['ext'], 'KP'),
        f'=IF(E{k}="0/0","",createF(C{k},ROW()))'
    ]]
    sheets.append(path, row)
    return True

def hq(proj, pic_url): # the url may not be the real url
    path = get_path('HQ')
    k = sheets.count_rows(path) + 1
    path.col = 'A:M'
    path.row = k
    row = [[
        f"'{proj.ino}", f"'{proj.title}", f"'{proj.pid}", STATE_MAP[5], '0/0', '', '',
        f'=HYPERLINK("{URL}/p?p={proj.pid}&s=HQ&r="&ROW(),"[人员]")',
        hyperlink(proj.urls['doc'], 'GG'),
        hyperlink(proj.urls['ext'], 'KP'),
        hyperlink(proj.urls['mic'], 'PY'),
        hyperlink(pic_url, 'SJ'),
        f'=IF(E{k}="","",createF(C{k},ROW()))'
    ]]
    sheets.append(path, row)
    return True
