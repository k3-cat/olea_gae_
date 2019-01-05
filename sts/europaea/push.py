from . import sheets, append, files
from .common import get_path, hyperlink


def fy(proj, row):
    proj['ssc'] = 'KP'
    path = get_path('FY')
    path.row = row
    append.kp((proj))
    sheets.del_line(path)
    return True

def kp(proj, row):
    proj['ssc'] = 'PY'
    path = get_path('KP')
    path.row = row
    append.py(proj)
    append.sj(proj)
    sheets.del_line(path)
    return True

def sj(proj, row):
    if proj['ssc'] == 'ps':
        proj['ssc'] = 'PY'
    elif proj['ssc'] == 'hs':
        proj['ssc'] = 'HQ'

        path = get_path('HQ')
        path.col = 'D'
        path.row = '2:'
        for i, pid_ in enumerate(sheets.get_values(path), 2):
            if proj.pid == pid_:
                path.row = i
                break
        else:
            return False

        path.col = 'K'
        sheets.set_values(path, [[hyperlink(proj['ids.pic'], 'SJ')]])
    else:
        return False
    path = get_path('PY')
    path.row = row
    sheets.del_line(path)
    return True

def py(proj, row):
    if proj['ssc'] == 'ps':
        proj['ssc'] = 'hs'
        if not proj['ids.pic']:  # 进度开始后一定会创建文件夹
            pic_id_ = '{未知}'
        else:   # 状态带s说明一定未完成
            pic_id_ = '{绘制中}'
    elif proj['ssc'] == 'PY':
        proj['ssc'] = 'HQ'
        pic_id_ = proj['ids.pic']
    path = get_path('PY')
    path.row = row
    append.hq(proj, pic_id_)
    sheets.del_line(path)
    return True

def hq(proj, row):
    proj['ssc'] = 'UP'
    path = get_path('HQ')
    path.row = row
    sheets.del_line(path)
    return True

def lb(proj, row, vid_url):
    proj['ssc'] = '00'
    path = get_path('LB')
    path.col = 'F'
    path.row = row
    sheets.set_values(path, [[vid_url]])
    files.clean(proj)
    return True
