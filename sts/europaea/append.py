from .GoogleIO import sheet
from . import get_path, hyperlink


def fy(projs):
    path = get_path('KP')
    k = sheet.count_rows(path) + 1
    path.col = 'A:M'
    path.row = f'k:{k+len(projs)}'
    rows = list()
    for i, proj in enumerate(projs, k):
        rows.append([[proj.ino, proj.title, '', proj.pid, '2 - 缺人', '', '', '人员',
                      hyperlink(proj.urls['doc'], 'FY'), '']])
    sheet.append(path, rows)
    return True

def kp(projs):
    path = get_path('KP')
    k = sheet.count_rows(path) + 1
    path.col = 'A:M'
    path.row = f'k:{k+len(projs)}'
    rows = list()
    for i, proj in enumerate(projs, k):
        rows.append([[proj.ino, proj.title, '', proj.pid, '9 - 未知', '0/0', '', '', False, '人员',
                      hyperlink(proj.urls['doc'], 'GG'),
                      f'=IF(F{i}="0/0","",createDoc(D{i},ROW()))',
                      f'=IF(I{i},push(D{i},ROW()),"")']])
    sheet.append(path, rows)
    return True

def ms(proj):
    path = get_path('MS')
    k = sheet.count_rows(path) + 1
    path.col = 'A:M'
    path.row = k
    row = [[proj.ino, proj.title, '', proj.pid, '', '', False, '人员',
            hyperlink(proj.urls['doc'], 'GG'),
            hyperlink(proj.urls['ext'], 'KP'),
            f'=IF(G{k}="","",createForder(D{k},ROW()))',
            f'=IF(OR(F{k},H{k}),push(D{k},ROW()),"")']]
    sheet.append(path, row)
    return True

def py(proj):
    path = get_path('PY')
    k = sheet.count_rows(path) + 1
    path.col = 'A:L'
    path.row = k
    row = [[proj.ino, proj.title, '', proj.pid, '2 - 缺人', '0/0', '', '', '人员',
            hyperlink(proj.urls['doc'], 'GG'),
            hyperlink(proj.urls['ext'], 'KP'),
            f'=IF(F{k}="0/0","",createForder(D{k},ROW()))']]
    sheet.append(path, row)
    return True

def hq(proj, pic_url): # the url may not be the real url
    path = get_path('HQ')
    k = sheet.count_rows(path) + 1
    path.col = 'A:M'
    path.row = k
    row = [[proj.ino, proj.title, '', proj.pid, f'=IF(F{k},"1 - 施工中","2 - 缺人")', '', False,
            hyperlink(proj.urls['doc'], 'GG'),
            hyperlink(proj.urls['ext'], 'KP'),
            hyperlink(proj.urls['mic'], 'PY'),
            hyperlink(pic_url, 'MS'),
            f'=IF(G{k}!="","",createForder(D{k},ROW()))',
            f'=IF(H{k},push(D{k},ROW()),"")']]
    sheet.append(path, row)
    return True
