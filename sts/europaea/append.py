from .google_io import sheets
from .common import get_path, hyperlink


def fy(projs):
    path = get_path('KP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:M'
    path.row = f'k:{k+len(projs)}'
    rows = list()
    for i, proj in enumerate(projs, k):
        rows.append([[proj.ino, proj.title, proj.pid, '2 - 缺人', '', '', '人员',
                      hyperlink(proj.urls['doc'], 'FY'), '']])
    sheets.append(path, rows)
    return True

def kp(projs):
    path = get_path('KP')
    k = sheets.count_rows(path) + 1
    path.col = 'A:M'
    path.row = f'k:{k+len(projs)}'
    rows = list()
    for i, proj in enumerate(projs, k):
        rows.append([[proj.ino, proj.title, proj.pid, '5 - 未知', '0/0', '', '', False, '人员',
                      hyperlink(proj.urls['doc'], 'GG'),
                      f'=IF(D{i}="1 - 施工中",createDoc(C{i},ROW()),"")',
                      f'=IF(H{i},push(C{i},D{i},ROW()),"")']])
    sheets.append(path, rows)
    return True

def ms(proj):
    path = get_path('MS')
    k = sheets.count_rows(path) + 1
    path.col = 'A:M'
    path.row = k
    row = [[proj.ino, proj.title, proj.pid, '5 - 未知', '', '', False, '人员',
            hyperlink(proj.urls['doc'], 'GG'),
            hyperlink(proj.urls['ext'], 'KP'),
            f'=IF(D{k}="1 - 施工中",createDoc(C{k},ROW()),"")',
            f'=IF(G{k}),push(C{k},D{k},ROW()),"")']]
    sheets.append(path, row)
    return True

def py(proj):
    path = get_path('PY')
    k = sheets.count_rows(path) + 1
    path.col = 'A:L'
    path.row = k
    row = [[proj.ino, proj.title, proj.pid, '2 - 缺人', '0/0', '', '', '人员',
            hyperlink(proj.urls['doc'], 'GG'),
            hyperlink(proj.urls['ext'], 'KP'),
            f'=IF(E{k}="0/0","",createForder(C{k},ROW()))']]
    sheets.append(path, row)
    return True

def hq(proj, pic_url): # the url may not be the real url
    path = get_path('HQ')
    k = sheets.count_rows(path) + 1
    path.col = 'A:M'
    path.row = k
    row = [[proj.ino, proj.title, proj.pid, f'=IF(E{k},"1 - 施工中","2 - 缺人")', '', False,
            hyperlink(proj.urls['doc'], 'GG'),
            hyperlink(proj.urls['ext'], 'KP'),
            hyperlink(proj.urls['mic'], 'PY'),
            hyperlink(pic_url, 'MS'),
            f'=IF(E{k}="","",createForder(C{k},ROW()))',
            f'=IF(F{k},push(C{k},ROW()),"")']]
    sheets.append(path, row)
    return True
