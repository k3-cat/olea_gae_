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
        obj = self.D
        for key in kg:
            obj = obj[key]
        return obj

    def __setitem__(self, key_g, value):
        kg = key_g.split('.')
        obj = self.D
        for i, key in enumerate(kg, 1):
            if i != len(kg):
                obj = obj[key]
            else:
                obj[key] = value
        self.temp[key_g] = value

    def __iter__(self):
        return self.D.__iter__()

    def clear_temp(self):
        self.temp.clear()

    def to_dict(self):
        return self.D


class User(PDict):
    @staticmethod
    def generate_pid():
        return ''.join(random.choices(PID_ALPHABET, k=3))

    @staticmethod
    def find_uid(nickname):
        doc = db.collection(u'users').where('nickname', '==', nickname).get()[0]
        return User(doc.id, dict_=doc.to_dict())

    def __init__(self, uid, info=None, dict_=None):
        if not uid:
            uid = User.generate_pid()
        self.uid = uid
        self.Irec = db.collection('users').document(uid)
        if not dict_:
            dict_ = self.Irec.get().to_dict()
            if not dict_:
                dict_ = info
                self.Irec.set(dict_)
        super().__init__(dict_)

    def _save(self):
        self.Irec.update(self.temp)
        self.clear_temp()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._save()

    def is_root(self):
        return self['root']


class Staff:
    STAFF_GROUP = ('FY', 'KP', 'PY', 'SJ', 'HQ')

    def __init__(self, proj, dict_):
        self.proj = proj
        self.users = dict()
        for sc in Staff.STAFF_GROUP:
            for uid in dict_[sc]:
                self.users[uid] = User(uid)
        self.D = dict_

    def __getitem__(self, key):
        return self.D[key]

    def set_req(self, sc, req):
        self.proj[f'req.{sc}'] = int(req)

    def get_state(self, sc):
        if not self.D[sc]:
            return 5
        if len(self.D[sc]) < self.proj[f'req.{sc}']:
            return 2
        for uid in self.D[sc]:
            if not self.users[uid][f'proj.{self.proj.pid}.{sc}.finish']:
                return 1
        return 0

    def add_staff(self, sc, uid, job):
        if uid in self.proj[f'staff.{sc}']:
            return
        self.users[uid] = User(uid)
        self.users[uid][f'proj.{self.proj.pid}.{sc}.finish'] = False
        self.proj[f'staff.{sc}.{uid}'] = job

    def finish_job(self, sc, uid):
        self.users[uid][f'proj.{self.proj.pid}.{sc}.finish'] = True

    def list_staff(self, sc_range=STAFF_GROUP, not_finish=None):
        result = list()
        for sc in sc_range:
            staff = list()
            for uid in self.D:
                if self.users[uid][f'proj.{self.proj.pid}.{sc}.finish'] != not_finish:
                    staff.append(uid)
            result.append(f'{sc}: {", ".join(staff)}')
        return '| '.join(result)

    def detials(self, sc):
        result = list()
        for uid in self.D[sc]:
            result.append({
                'u': self.users[uid]['nickname'],
                'j': self.D[sc][uid],
                'f': self.users[uid][f'proj.{self.proj.pid}.{sc}.finish']})
        return result


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
        dict_['staff'] = Staff(self, dict_['staff'])
        self.D = dict_

    def save(self):
        self.Irec.update(self.temp)
        self.clear_temp()

    @property
    def ssc_display(self):
        return Project.SSC2D_MAP[self['ssc']]

    @property
    def name(self):
        if self['ino'] == '':
            return self['title']
        return f'SCP-{self["ino"]} - {self["title"]}'
