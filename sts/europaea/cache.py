import time

from .common import get_path
from .global_value import PATH_MAP
from .google_io import sheets


class PidLineCache:
    pid_map = dict()
    pid_list = dict()
    time = {sc: 0 for sc in PATH_MAP}

    @classmethod
    def update_list(cls, sc):
        cls.time[sc] = time.time()
        cls.pid_list[sc] = list()
        path = get_path(sc)
        path.col = 'C'
        path.row = '2:'
        for line in sheets.get_values(path):
            if not line:
                cls.pid_list[sc].append(None)
            else:
                cls.pid_list[sc].append(line[0])

    @classmethod
    def update(cls, sc):
        now = time.time()
        if sc not in cls.time or now - cls.time[sc] > 900:
            cls.update_list(sc)
        cls.pid_map[sc] = dict()
        for k, pid in enumerate(cls.pid_list[sc], 2):
            if pid:
                cls.pid_map[sc][pid] = k

    @classmethod
    def append(cls, sc, pid):
        cls.pid_list[sc].append(pid)
        cls.update(sc)

    @classmethod
    def delete(cls, sc, pid):
        cls.pid_list[sc].remove(pid)
        cls.update(sc)

    @classmethod
    def get(cls, sc, pid):
        return cls.pid_map[sc][pid]


class PageCache:
    page_soup = dict()

    @staticmethod
    def clear_cache():
        PageCache.page_soup.clear()
