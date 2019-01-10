from . import sheets, append
from .common import get_path, hyperlink


def fy(proj, pos):
    proj['ssc'] = 'KP'
    append.kp((proj))
    path = get_path('FY')
    path.row = pos
    sheets.del_line(path)
    return True

def kp(proj, pos):
    proj['ssc'] = 'pu'
    append.py(proj)
    append.uj(proj)
    path = get_path('KP')
    path.row = pos
    sheets.del_line(path)
    return True

def uj(proj, pos):
    if proj['ssc'] == 'pu':
        proj['ssc'] = 'PY'
    elif proj['ssc'] == 'hu':
        proj['ssc'] = 'HQ'

        path_ = get_path('HQ')
        path_.col = 'C'
        path_.row = '2:'
        for i, pid_ in enumerate(sheets.get_values(path_), 2):
            try:
                pid = pid_[0]
            except ValueError:
                continue
            if proj.pid == pid:
                path_.row = i
                break
        else:
            return False

        path_.col = 'K'
        sheets.set_values(path_, [[hyperlink(proj['ids.pic'], 'UJ')]])
    else:
        return False
    path = get_path('UJ')
    path.row = pos
    sheets.del_line(path)
    return True

def py(proj, pos):
    if proj['ssc'] == 'pu':
        proj['ssc'] = 'hu'
        if not proj['ids.pic']:  # 进度开始后一定会创建文件夹
            pic_id_ = '{未知}'
        else:   # 状态带s说明一定未完成
            pic_id_ = '{绘制中}'
    elif proj['ssc'] == 'PY':
        proj['ssc'] = 'HQ'
        pic_id_ = proj['ids.pic']
    else:
        return False
    append.hq(proj, pic_id_)
    path = get_path('PY')
    path.row = pos
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
    proj.finish()
    path = get_path('LB')
    path.col = 'F'
    path.row = pos
    sheets.set_values(path, [[vid_url]])
    return True
