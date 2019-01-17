from . import append, sheets
from .common import PidLineCache, get_path, hyperlink


def fy(proj):
    proj['ssc'] = 'KP'
    append.kp((proj))
    path = get_path('FY')
    path.row = PidLineCache.get('FY', proj.pid)
    sheets.del_line(path)
    return True

def kp(proj):
    proj['ssc'] = 'pu'
    append.py(proj)
    append.uj(proj)
    path = get_path('KP')
    path.row = PidLineCache.get('KP', proj.pid)
    sheets.del_line(path)
    return True

def uj(proj):
    if proj['ssc'] == 'pu':
        proj['ssc'] = 'PY'
    elif proj['ssc'] == 'hu':
        proj['ssc'] = 'HQ'
        path_ = get_path('HQ')
        path_.col = 'K'
        path_.row = PidLineCache.get('HQ', proj.pid)
        sheets.set_values(path_, [[hyperlink(proj['ids.pic'], 'UJ')]])
    else:
        return False
    path = get_path('UJ')
    path.row = PidLineCache.get('UJ', proj.pid)
    sheets.del_line(path)
    return True

def py(proj):
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
    path.row = PidLineCache.get('PY', proj.pid)
    sheets.del_line(path)
    return True

def hq(proj):
    proj['ssc'] = 'UP'
    path = get_path('HQ')
    path.row = PidLineCache.get('HQ', proj.pid)
    sheets.del_line(path)
    return True

def lb(proj, vid_url):
    proj['ssc'] = '00'
    proj.finish()
    path = get_path('LB')
    path.col = 'F'
    path.row = PidLineCache.get('LB', proj.pid)
    if 'youtu.be' in vid_url:
        site = 'YT'
    elif 'youtube' in vid_url:
        vid_url = f'https://youtu.be/{vid_url[32:43]}'
        site = 'YT'
    else:
        site = 'BB'
    sheets.set_values(path, [[hyperlink(vid_url, site)]])
    return True
