import random

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import google.cloud.exceptions


cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'olea-0',
})
db = firestore.client()


class DDict:
    def __init__(self, Idict=None):
        if not Idict:
            Idict = dict()
        self.Idict = Idict

    def __len__(self):
        return len(self.Idict)

    def __iter__(self):
        return self.Idict.__iter__()

    def __getattr__(self, name):
        return self.Idict[name]

    def __setattr__(self, name, value):
        if name[0] == 'I':
            self.__dict__[name] = value
        else:
            self.Idict[name] = value

class StaffGroup(DDict):
    def __init__(self, source):
        for key in source:
            source[key] = Staff(dict_=source[key])
        super().__init__(source)

    def __getitem__(self, key):
        return self.Idict[key]

    def to_dict(self):
        temp_dict = self.Idict.copy()
        for key in temp_dict:
            temp_dict[key] = temp_dict[key].to_dict()
        return temp_dict

class PDict:
    def __init__(self, dict_=None):
        if not dict_:
            dict_ = dict()
        self.dict_ = dict_
        self.temp = dict()

    def __len__(self):
        return len(self.dict_)

    def __getitem__(self, key):
        return self.dict_[key]

    def __setitem__(self, key, value):
        self.dict_[key] = value
        self.temp[key] = value

    def __iter__(self):
        return self.dict_.__iter__()

    def clear_temp(self):
        self.temp.clear()

    def to_dict(self):
        return self.dict_

class Staff(PDict):
    @property
    def state(self):
        if self.is_empty():
            return 5
        for member in self.dict_:
            if member[0] == '':
                return 2
            if not member[2]:
                return 1
        return 0

    @property
    def all(self):
        return ', '.join(self.dict_.keys())

    def _part(self, finish):
        result = list()
        for member in self.dict_:
            if member[2] == finish:
                result.append(f'{member[0]}({member[1]})')
        return ', '.join(result)

    @property
    def finished(self):
        return self._part(True)

    @property
    def unfinished(self):
        return self._part(False)

    def is_empty(self):
        if self.dict_:
            return False
        return True


class Project(DDict):
    SSC = {
        'F': '翻译',
        'K': '编篡文案',
        'P': '配音',
        'p': '配音+绘制插图',
        'H': '后期',
        'h': '后期+绘制插图',
        'U': '上传'
    }

    PID_ALPHABET = (
        '0123456789aAbBcC'
        'dDeEfFgGhHiIjJkK'
        'lLmMnNoOpPqQrRsS'
        'tTuUvVwWxXyYzZ-_'
    )

    @staticmethod
    def generate_pid():
        return ''.join(random.choices(Project.PID_ALPHABET, k=5))

    @staticmethod
    def get_empty_proj(info):
        return {
            'ino': info[0],
            'title': info[1],
            'ssc': '',
            'p_c': False,               # pic_checked
            'urls': {'doc': info[2], 'ext': None, 'mic': None, 'aep': None},
            'staff': {'t': {}, 'T': {}, 'C': {}, 'P': {}, 'D': {}, 'F': {}}
        }

    def __init__(self, pid, info=None):
        super().__init__()
        if not pid:
            pid = Project.generate_pid()
        self.Ipid = pid
        self.Irec = db.collection('projects').document(pid)
        self.Itemp = dict()
        try:
            dict_ = self.Irec.get().to_dict()
        except google.cloud.exceptions.NotFound:
            dict_ = Project.get_empty_proj(info)
            self.Irec.set(dict_)
        self._refresh(dict_)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name[0] != 'I':
            self.Itemp[name] = value

    def save(self):
        temp = self.Itemp.copy()
        for change in self.urls.temp:
            temp[f'urls.{change}'] = self.urls.temp[change]
        for group in self.staff:
            for change in self.staff[group].temp:
                temp[f'staff.{group}.{change}'] = self.staff[group].temp[change]
            self.staff[group].clear_temp()
        self.Irec.update(temp)
        self._refresh(self.Irec.get().to_dict())
        self.clear_temp()

    def _refresh(self, dict_):
        dict_['staff'] = StaffGroup(dict_['staff'])
        dict_['urls'] = PDict(dict_['urls'])
        self.Idict = dict_

    def clear_temp(self):
        self.Itemp.clear()

    @property
    def pid(self):
        return self.Ipid

    @property
    def ssc_display(self):
        return Project.SSC[self.ssc]

    @property
    def name(self):
        if self.ino == '':
            return self.title
        return f'SCP-{self.ino} {self.title}'

    @property
    def all_staff(self):
        staff = list()
        if self.staff.T.state == 0:
            staff.append(f'T: {self.staff.t.all}; {self.staff.T.all}')
        if self.staff.C.state == 0:
            staff.append(f'C: {self.staff.C.all}')
        if self.staff.P.state == 0:
            staff.append(f'P: {self.staff.P.all}')
        if self.staff.D.state == 0:
            staff.append(f'D: {self.staff.D.all}')
        if self.staff.F.state == 0:
            staff.append(f'F: {self.staff.F.all}')
        return ' | '.join(staff)
