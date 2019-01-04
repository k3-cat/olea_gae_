import random

import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'olea-db',
})
db = firestore.client()

PID_ALPHABET = (
    '0123456789aAbBcC'
    'dDeEfFgGhHiIjJkK'
    'lLmMnNoOpPqQrRsS'
    'tTuUvVwWxXyYzZ-_'
)


class PDict:
    def __init__(self, dict_=None):
        if not dict_:
            dict_ = dict()
        self.D = dict_
        self.temp = dict()

    def __len__(self):
        return len(self.D)

    def __getitem__(self, key_g):
        kg = key_g.split('.')
        obj = self.D[kg[0]]
        for key in kg:
            obj = obj[key]
        return obj

    def __setitem__(self, key_g, value):
        kg = key_g.split('.')
        obj = self.D[kg[0]]
        for key in kg:
            obj = obj[key]
        obj = value
        self.temp[key_g] = value

    def __iter__(self):
        return self.D.__iter__()

    def clear_temp(self):
        self.temp.clear()

    def to_dict(self):
        return self.D


class User(PDict):
    @staticmethod
    def get_empty_user():
        return {
            'email': None,
            'gmail': None,
            'name': None
        }

    def __init__(self, name):
        self.name = name
        self.Irec = db.collection('users').document(name)
        dict_ = self.Irec.get().to_dict()
        if not dict_:
            dict_ = User.get_empty_user()
            self.Irec.set(dict_)
        super().__init__(dict_)

    def _save(self):
        self.Irec.update(self.temp)
        self.clear_temp()

    def __setitem__(self, key, value):
        super().__init__(key, value)
        self._save()


class Staff:
    STAFF_GROUP = ('FY', 'KP', 'PY', 'SJ', 'HQ')

    def __init__(self, proj, dict_):
        self.proj = proj
        for sc in Staff.STAFF_GROUP:
            for member in dict_[sc]:
                dict_[sc][member] = User(dict_[sc][member])
        self.D = dict_

    def set_req(self, sc, req):
        self.proj[f'req.{sc}'] = req

    def get_state(self, sc):
        if not self.D[sc]:
            return 5
        if len(self.D[sc]) < self.proj[f'req.{sc}']:
            return 2
        for member in self.D:
            if not self.D[member][f'{self.proj.pid}.{sc}.finish']:
                return 1
        return 0

    def add_staff(self, sc, name, job):
        self.D[name] = User(name)
        self.D[name][f'{self.proj.pid}.{sc}.job'] = job

    def finish_job(self, sc, name):
        self.D[name][f'{self.proj.pid}.{sc}.finish'] = True

    def list_staff(self, sc_range=Staff.STAFF_GROUP, not_finish=None):
        result = list()
        for sc in sc_range:
            staff = list()
            for member in self.D:
                if self.D[member][f'{self.proj.pid}.{sc}.finish'] != not_finish:
                    staff.append(member)
            result.append(f'{sc}: {", ".join(staff)}')
        return '| '.join(result)

class Project(PDict):
    SSC2D_MAP = {
        'F': '翻译',
        'K': '编篡文案',
        'P': '配音',
        'p': '配音+绘制插图',
        'H': '后期',
        'h': '后期+绘制插图',
        'U': '上传',
        'C': '完成'
    }

    @staticmethod
    def generate_pid():
        return ''.join(random.choices(PID_ALPHABET, k=5))

    @staticmethod
    def get_empty_proj(info):
        if info[2] == '':
            doc_id = None
        else:
            doc_id = info[2]
        return {
            'ino': info[0],
            'title': info[1],
            'ssc': '',
            'p_c': False,               # pic_checked
            'ids': {'doc_id': doc_id, 'ext_id': None, 'mic_id': None, 'aep_id': None},
            'req': {'FY': 0, 'KP': 0, 'PY': 0, 'SJ': 0, 'HQ': 0},
            'staff': {'FY': {}, 'KP': {}, 'PY': {}, 'SJ': {}, 'HQ': {}}
        }

    def __init__(self, pid, info=None):
        super().__init__()
        if not pid:
            pid = Project.generate_pid()
        self.pid = pid
        self.Irec = db.collection('projects').document(pid)
        self.Itemp = dict()
        dict_ = self.Irec.get().to_dict()
        if not dict_:
            dict_ = Project.get_empty_proj(info)
            self.Irec.set(dict_)
        self._refresh(dict_)

    def save(self):
        self.Irec.update(self.temp)
        self._refresh(self.Irec.get().to_dict())
        self.clear_temp()

    def _refresh(self, dict_):
        dict_['staff'] = Staff(self, dict_['staff'])
        self.D = dict_

    @property
    def ssc_display(self):
        return Project.SSC2D_MAP[self['ssc']]

    @property
    def name(self):
        if self['ino'] == '':
            return self['title']
        return f'SCP-{self["ino"]} - {self["title"]}'
