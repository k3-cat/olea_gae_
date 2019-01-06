from . import sheets, append
from .common import get_path, hyperlink


def fy(proj, pos):
    proj['ssc'] = 'KP'
    path = get_path('FY')
    path.row = pos
    append.kp((proj))
    sheets.del_line(path)
    return True

def kp(proj, pos):
    proj['ssc'] = 'PY'
    path = get_path('KP')
    path.row = pos
    append.py(proj)
    append.sj(proj)
    sheets.del_line(path)
    return True

def sj(proj, pos):
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
    path.row = pos
    sheets.del_line(path)
    return True

def py(proj, pos):
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
    path.row = pos
    append.hq(proj, pic_id_)
    sheets.del_line(path)
    return True

def hq(proj, pos):
    proj['ssc'] = 'UP'
    path = get_path('HQ')
    path.row = pos
    sheets.del_line(path)
    return True

def lb(proj, pos, vid_url):
    proj['ssc'] = '00'
    path = get_path('LB')
    path.col = 'F'
    path.row = pos
    sheets.set_values(path, [[vid_url]])
    proj.finish()
    return True
