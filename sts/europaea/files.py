from .global_value import URLS_MAP
from .google_io import drive
from .records import set_hyperlink


def create(proj, sc):
    name = proj.name
    if '}' in name:
        return False
    if proj[f'ids.{URLS_MAP[sc][1]}']:
        id_ = proj[f'ids.{URLS_MAP[sc][1]}']
    else:
        if sc == 'KP':
            type_ = 'doc'
        elif sc in ('UJ', 'PY', 'HQ'):
            type_ = 'folder'
        id_ = drive.new(name, type_, URLS_MAP[sc][0])
        proj[f'ids.{URLS_MAP[sc][1]}'] = id_
        proj.save()
    set_hyperlink(proj.pid, sc, id_)
    return True


def clean(proj):
    if proj[f'ids.{URLS_MAP["KP"][1]}']:
        drive.move(proj[f'ids.{URLS_MAP["KP"][1]}'], URLS_MAP['KP'][2])
    if proj[f'ids.{URLS_MAP["UJ"][1]}']:
        drive.move(proj[f'ids.{URLS_MAP["UJ"][1]}'], URLS_MAP['UJ'][2])
    if proj[f'ids.{URLS_MAP["PY"][1]}']:
        drive.delete(proj[f'ids.{URLS_MAP["PY"][1]}'])
    if proj[f'ids.{URLS_MAP["HQ"][1]}']:
        drive.delete(proj[f'ids.{URLS_MAP["HQ"][1]}'])
    return True
