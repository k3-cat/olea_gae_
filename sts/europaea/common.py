import time

from . import sheets


URL = 'https://olea-db.appspot.com'

PATH_MAP = {'LB': ('1UAD7PSiVtuWazMakg7jDtHXu9PqC5CQBcx8YZ4H4o7U', '配音'),
            'FY': ('1kSGUUmzjNk3NTuE8EU6LBuToz9NV3m430ZgxEkMnd7Q', '接稿'),
            'KP': ('146lz1z0sAv7dpJh4FWWOHccVy0eeLYJVCJS2eiTnTbs', '接稿'),
            'UJ': ('1WhC9U3hm0FVdvynnK8VPcBJskmovUp8NnwOO3ZFbxsI', '接稿'),
            'PY': ('1zkLzY8vSFHPoc6RKddbUeb8e3DG1e8hlZPU2h9u3jLQ', '接稿'),
            'HQ': ('1lsnWTV9IpUPmQpD3jijn5Tx9jkyHyD0wB-BrSNCm2Tg', '接稿')}

def get_path(code):
    return sheets.Path(id_=PATH_MAP[code][0], table=PATH_MAP[code][1])


HL_MAP = {'GG': ('http://scp-wiki-cn.wikidot.com/', '='),
          'FY': ('http://www.scp-wiki.net/', '-'),
          'KP': ('https://docs.google.com/document/d/', '~'),
          'PY': ('https://drive.google.com/drive/folders/', '<'),
          'UJ': ('https://drive.google.com/drive/folders/', '+'),
          'HQ': ('https://drive.google.com/drive/folders/', '#')}

def hyperlink(url_, type_):
    if not url_:
        return ''
    if '{' in url_:
        return url_
    return f'=HYPERLINK("{HL_MAP[type_][0]}{url_}","[{HL_MAP[type_][1]*4}]")'

STATE_MAP = {
    0: '0 - 完成',
    1: '1 - 施工中',
    2: '2 - 缺人',
    5: '5 - 初始',
    9: '9 - 错误',
}

SC2D_MAP = {
    'FY': '翻译',
    'KP': '科普',
    'PY': '配音',
    'UJ': '设计',
    'HQ': '后期'
}

class LbLineCache:
    cache = dict()
    time = 0

    @classmethod
    def update(cls):
        cls.cache.clear()
        path = get_path('LB')
        path.col = 'C'
        path.row = '2:'
        for k, line in enumerate(sheets.get_values(path), 2):
            if not line:
                continue
            cls.cache[line[0]] = k

    @classmethod
    def get(cls, pid):
        now = time.time()
        if now - cls.time > 120:
            LbLineCache.update()
        return LbLineCache.cache[pid]

class CreateLock:
    create_time = dict()

    @classmethod
    def check(cls, pid):
        now = time.time()
        for pid_ in cls.create_time:
            if now - cls.create_time[pid_] > 10:
                del cls.create_time[pid_]
        if pid in cls.create_time:
            return False
        cls.create_time[pid] = now
        return True
