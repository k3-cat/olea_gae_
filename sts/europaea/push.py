from . import append
from .cache import PidLineCache
from .common import get_path, hyperlink
from .google_io import sheets
from .records import update_m_process_info


def fy(proj):
    proj.add_ssc('KP')
    append.kp((proj,))
    path = get_path('FY')
    path.row = PidLineCache.get('FY', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True


def kp(proj):
    proj.add_ssc('PY')
    proj.add_ssc('UJ')
    proj.remove_ssc('KP')
    append.py(proj)
    append.uj(proj)
    path = get_path('KP')
    path.row = PidLineCache.get('KP', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True


def uj(proj):
    if 'HQ' in proj['ssc']:
        path_ = get_path('HQ')
        path_.col = 'K'
        path_.row = PidLineCache.get('HQ', proj.pid)
        sheets.set_values(path_, [[hyperlink(proj['ids.pic'], 'UJ')]])
    proj.remove_ssc('UJ')
    path = get_path('UJ')
    path.row = PidLineCache.get('UJ', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True


def py(proj):
    proj.add_ssc('HQ')
    proj.remove_ssc('PY')
    append.hq(proj)
    path = get_path('PY')
    path.row = PidLineCache.get('PY', proj.pid)
    sheets.del_line(path)
    update_m_process_info(proj)
    return True


def hq(proj):
    proj.add_ssc('UP')
    proj.remove_ssc('HQ')
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
        return '無效的鏈接'
    proj.add_ssc('00')
    proj.remove_ssc('UP')
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
