from . import sheets, append, files
from .common import get_path, hyperlink


def fy(proj, row):
    path = get_path('FY')
    path.col = 'G'
    path.row = row
    # record = sheet.get_values(path)[0][0]
    proj.ssc = 'K'
    append.kp((proj))
    sheets.del_line(path)
    return True

def kp(proj, row):
    path = get_path('KP')
    path.col = 'G:I'
    path.row = row
    # records = sheets.get_values(path)[0]
    proj.ssc = 'P'
    append.py(proj)
    append.sj(proj)
    sheets.del_line(path)
    return True

def sj(proj, row):
    pid = proj.pid
    path = get_path('PY')
    path.col = 'F:H'
    path.row = row
    # records = sheets.get_values(path)[0]
    if proj.ssc == 'p':
        proj.ssc = 'P'
    elif proj.ssc == 'h':
        proj.ssc = 'H'

        path = get_path('HQ')
        path.col = 'D'
        path.row = '2:'
        for i, pid_ in enumerate(sheets.get_values(path), 2):
            if pid == pid_:
                path.row = i
                break
        else:
            return False

        path.col = 'K'
        sheets.set_values(path, [[hyperlink(proj.urls['pic'], 'SJ')]])
    sheets.del_line(path)
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
    sheets.del_line(path)
    return True

def hq(proj, row):
    path = get_path('HQ')
    path.col = 'F'
    path.row = row
    # record = sheets.get_values(path)[0][0]
    proj.ssc = 'U'
    sheets.del_line(path)
    return True

def lb(proj, row, vid_url):
    path = get_path('LB')
    path.col = 'F'
    path.row = row
    sheets.set_values(path, [[vid_url]])
    files.clean(proj)
    return True
