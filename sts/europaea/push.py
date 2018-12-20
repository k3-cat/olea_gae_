from . import sheet
from . import get_path, hyperlink, append


def fy(proj, row):
    path = get_path('FY')
    path.col = 'G'
    path.row = row
    # record = sheet.get_values(path)[0][0]
    proj.ssc = 'K'
    append.kp((proj))
    sheet.del_line(path)
    return True

def kp(proj, row):
    path = get_path('KP')
    path.col = 'G:I'
    path.row = row
    records = sheet.get_values(path)[0]
    if records[0] != '' or (records[1] != '' and records[2]):
        path.col = 'I'
        sheet.set_values(path, [[False]])
        return False
    proj.ssc = 'P'
    append.py(proj)
    append.ms(proj)
    sheet.del_line(path)
    return True

def ms(proj, row):
    pid = proj.pid

    path = get_path('PY')
    path.col = 'F:H'
    path.row = row
    records = sheet.get_values(path)[0]
    if records[0] != '' or (records[1] != '' and records[2]):
        path.col = 'H'
        sheet.set_values(path, [[False]])
        return False
    if records[2]:
        proj.urls['pic'] = ''
    if proj.ssc == 'p':
        proj.ssc = 'P'
    elif proj.ssc == 'h':
        proj.ssc = 'H'

        path = get_path('HQ')
        path.col = 'D'
        path.row = '2:'
        for i, pid_ in enumerate(sheet.get_values(path), 2):
            if pid == pid_:
                path.row = i
                break
        else:
            return False

        path.col = 'K'
        sheet.set_values(path, [[hyperlink(proj.urls['pic'], 'MS')]])
    sheet.del_line(path)
    return True

def py(proj, row):
    path = get_path('PY')
    path.col = 'H'
    path.row = row
    # record = sheet.get_values(path)[0][0]
    if proj.ssc == 'p':
        proj.ssc = 'h'
        if proj.urls['pic'] == '0':
            pic_url_ = '{未知}'
        else:
            pic_url_ = '{绘制中}'
    elif proj.ssc == 'P':
        proj.ssc = 'H'
        pic_url_ = proj.urls['pic']
    append.hq(proj, pic_url_)
    sheet.del_line(path)
    return True

def hq(proj, row):
    path = get_path('HQ')
    path.col = 'F'
    path.row = row
    record = sheet.get_values(path)[0][0]
    proj.ssc = 'U'
    proj.staff.F = record
    sheet.del_line(path)
    return True
