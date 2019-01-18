import random
import time

import firebase_admin
from firebase_admin import credentials, firestore

from .files import clean


cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'olea-db',
})

db = firestore.client()


PID_ALPHABET = (
    '0123456789aAbBcC'
    'dDeEfFgGhHiIjJkK'
    'lLmMnNoOpPqQrRsS'
    'tTuUvVwWxXyYzZ_'
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
            try:
                obj = obj[key]
            except KeyError:
                return None
        return obj

    def __setitem__(self, key_g, value):
        kg = key_g.split('.')
        obj = self.D
        for i, key in enumerate(kg, 1):
            if key not in obj:
                obj[key] = dict()
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
    def find_uid(name):
        docs = db.collection(u'users').where('name', '==', name).get() # return a generator
        for doc in docs:
            return User(doc.id, dict_=doc.to_dict())

    def __init__(self, uid, dict_=None):
        self.uid = uid
        self.Irec = db.collection('users').document(uid)
        if not dict_:
            dict_ = self.Irec.get().to_dict()
            if not dict_:
                return
        super().__init__(dict_)

    def _save(self):
        if not self.temp:
            return
        self.Irec.update(self.temp)
        self.clear_temp()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._save()

    def info(self):
        user_info = dict()
        user_info['groups'] = self.D['groups']
        user_info['uid'] = self.uid
        return user_info

class Staff(PDict):
    def __init__(self, proj, dict_):
        self.proj = proj
        self.users = dict()
        for sc in dict_:
            for uid in dict_[sc]:
                self.users[uid] = User(uid)
        super().__init__(dict_)

    def set_req(self, sc, req):
        req = int(req)
        if req < 0 or req < len(self.proj[f'staff.{sc}']):
            return False
        self.proj[f'req.{sc}'] = req
        if sc not in self.proj['staff']:
            self.proj[f'staff.{sc}'] = dict()
        return True

    def get_state(self, sc):
        if sc not in self.proj[f'req']:
            return 5
        if self.proj[f'req'] == 0:
            return 4
        if sc not in self.D:
            return 9
        if len(self[sc]) < self.proj[f'req.{sc}']:
            return 2
        for uid in self[sc]:
            if self.users[uid][f'proj.{sc}.{self.proj.pid}.end'] is None:
                return 1
        return 0

    def add_staff(self, sc, uid, job):
        if len(self[sc]) >= self.proj[f'req.{sc}'] or uid in self.proj[f'staff.{sc}']:
            return False
        user = User(uid)
        if sc not in user.info()['groups']:
            return False
        user[f'proj.{sc}.{self.proj.pid}.start'] = time.time()
        self.users[uid] = user
        self.proj[f'staff.{sc}.{uid}'] = job
        return True

    def edit_staff(self, sc, uid, job):
        if uid not in self[sc]:
            return False
        self.proj[f'staff.{sc}.{uid}'] = job
        return True

    def finish_job(self, sc, uid):
        now = time.time()
        if now - self.users[uid][f'proj.{sc}.{self.proj.pid}.start'] < 3600:
            self.users[uid][f'proj.{sc}.{self.proj.pid}.end'] = 0
        else:
            self.users[uid][f'proj.{sc}.{self.proj.pid}.end'] = now
        return True


    def list_staff(self, sc_range):
        result = dict()
        for sc in sc_range:
            if not self[sc]:
                result[sc] = [[], []]
                continue
            staff = [[], []]
            for uid in self[sc]:
                if self.users[uid][f'proj.{sc}.{self.proj.pid}.end']:
                    staff[0].append(self.users[uid]['name'])
                else:
                    staff[1].append(self.users[uid]['name'])
            result[sc] = staff
        return result

    def detials(self, sc):
        result = list()
        for uid in self[sc]:
            result.append({
                'uid': uid,
                'u': self.users[uid]['name'],
                'j': self[sc][uid],
                'f': self.users[uid][f'proj.{sc}.{self.proj.pid}.end'] is not None})
        return result

class Project(PDict):
    SSC2D_MAP = {
        'FY': '翻译',
        'KP': '编篡文案',
        'PY': '配音',
        'pu': '配音+绘图',
        'HQ': '后期',
        'hu': '后期+绘图',
        'UP': '上传',
        '00': '完成'
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
            'ids': {'doc': doc_id},
            'req': {},
            'staff': {}
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
        if not self.temp:
            return
        self.Irec.update(self.temp)
        self.clear_temp()

    def finish(self):
        clean(self)

    @property
    def ssc_display(self):
        return Project.SSC2D_MAP[self['ssc']]

    @property
    def name(self):
        if self['ino'] == '':
            return self['title']
        return f'SCP-{self["ino"]} - {self["title"]}'
