import time

from .GoogleIO import sheet


PATH_MAP = {'LB': ('1UAD7PSiVtuWazMakg7jDtHXu9PqC5CQBcx8YZ4H4o7U', '配音'),
            'FY': ('1kSGUUmzjNk3NTuE8EU6LBuToz9NV3m430ZgxEkMnd7Q', '接稿'),
            'KP': ('146lz1z0sAv7dpJh4FWWOHccVy0eeLYJVCJS2eiTnTbs', '接稿'),
            'MS': ('1WhC9U3hm0FVdvynnK8VPcBJskmovUp8NnwOO3ZFbxsI', '接稿'),
            'PY': ('1zkLzY8vSFHPoc6RKddbUeb8e3DG1e8hlZPU2h9u3jLQ', '接稿'),
            'HQ': ('1lsnWTV9IpUPmQpD3jijn5Tx9jkyHyD0wB-BrSNCm2Tg', '接稿')}

def get_path(code):
    return sheet.Path(id_=PATH_MAP[code][0], table=PATH_MAP[code][1])


LINK_PRE_MAP = {'GG': ('http://scp-wiki-cn.wikidot.com/', '='),
                'FY': ('http://www.scp-wiki.net/', '-'),
                'KP': ('https://docs.google.com/document/d/', '~'),
                'MS': ('https://drive.google.com/drive/folders/', '+'),
                'PY': ('https://drive.google.com/drive/folders/', '<'),
                'HQ': ('https://drive.google.com/drive/folders/', '#')}

def hyperlink(url_, type_):
    if url_ == '':
        return ''
    if '{' in url_:
        return url_
    return f'=HYPERLINK("{LINK_PRE_MAP[type_][0]}{url_}","[f{LINK_PRE_MAP[type_][1]*4}]")'
