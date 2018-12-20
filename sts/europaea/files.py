from . import drive
from .records import set_hyperlink


MAP = {
    'KP': ('15B4w3PMbrqCPSKYvTHlSvEEOA-1ioEgL', 'ext'),
    'MS': ('13rnCWi9nwNWH4fXLRvxSsN5nxaWPR3V4', 'pic'),
    'PY': ('1e4zS1wVm5umIUOShaZx0GN2M4fEgV1en', 'mic'),
    'HQ': ('1J6OD7L0kt_c8eqV8cEN0C0dK2VApGIML', 'aep')
}

def create(sc, proj, row, is_folder):
    name = proj.name
    if '}' in name:
        return False
    if is_folder:
        id_ = drive.new(MAP[sc][0], name, type_='folder')
    else:
        id_ = drive.new(MAP[sc][0], name, type_='doc')
    proj.urls[MAP[sc][1]] = id_
    set_hyperlink(sc, row, id_)
    return True
