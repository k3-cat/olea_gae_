from .common import get_path
from .global_value import PATH_MAP
from .google_io import sheets


def fetch_pid_pos(sc):
    pid_list = list()
    path = get_path(sc)
    path.col = 'C'
    path.row = '2:'
    for line in sheets.get_values(path):
        if not line:
            pid_list.append(None)
        else:
            pid_list.append(line[0])
    pid_map = dict()
    for k, pid in enumerate(pid_list, 2):
        if pid:
            pid_map[pid] = k
    return pid_map


class PidLineCache:
    pid_map = {sc: fetch_pid_pos(sc) for sc in PATH_MAP}

    @classmethod
    def append(cls, sc, pid):
        cls.pid_map[sc][pid] = len(cls.pid_map[sc]) + 2

    @classmethod
    def delete(cls, sc, pid):
        pos = cls.pid_map[sc][pid]
        del cls.pid_map[sc][pid]
        for pid_, line_no in cls.pid_map[sc].items():
            if line_no > pos:
                cls.pid_map[sc][pid_] -= 1

    @classmethod
    def get(cls, sc, pid):
        return cls.pid_map[sc][pid]


class PageCache:
    page_soup = dict()

    @staticmethod
    def clear_cache():
        PageCache.page_soup.clear()
