from . import append, sheets
from .common import PidLineCache, get_path, hyperlink
from .records import update_m_process_info


def fy(proj):
    proj['ssc'] = 'KP'
    append.kp((proj))
    path = get_path('FY')
    path.row = PidLineCache.get('FY', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True

def kp(proj):
    proj['ssc'] = 'pu'
    append.py(proj)
    append.uj(proj)
    path = get_path('KP')
    path.row = PidLineCache.get('KP', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
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
    path = get_path('UJ')
    path.row = PidLineCache.get('UJ', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True

def py(proj):
    if proj['ssc'] == 'pu':
        proj['ssc'] = 'hu'
    elif proj['ssc'] == 'PY':
        proj['ssc'] = 'HQ'
    append.hq(proj)
    path = get_path('PY')
    path.row = PidLineCache.get('PY', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True

def hq(proj):
    proj['ssc'] = 'UP'
    path = get_path('HQ')
    path.row = PidLineCache.get('HQ', proj.pid)
    append.up(proj)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True

def up(proj, vid_url):
    if 'youtube.com' in vid_url:
        vid_url = f'https://youtu.be/{vid_url[32:43]}'
        site = 'YT'
    elif 'youtu.be' in vid_url:
        site = 'YT'
    elif 'bilibili.com' in vid_url:
        site = 'BB'
    else:
        return False
    proj['ssc'] = '00'
    proj.finish()
    path = get_path('LB')
    path.col = 'F'
    path.row = PidLineCache.get('LB', proj.pid)
    sheets.set_values(path, [[hyperlink(vid_url, site)]])

    path_ = get_path('UP')
    path_.row = PidLineCache.get('UP', proj.pid)
    sheets.del_line(path_)
    update_m_process_info(proj)
    return True
