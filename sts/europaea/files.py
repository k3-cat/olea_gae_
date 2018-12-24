from . import drive
from .records import set_hyperlink


URLS_MAP = {
    'KP': ('15B4w3PMbrqCPSKYvTHlSvEEOA-1ioEgL', 'ext', '1QH0uMkhhCfWVq8Cq0CdV7Tb4damKqagw'),
    'SJ': ('13rnCWi9nwNWH4fXLRvxSsN5nxaWPR3V4', 'pic', '1Xh2ynRMm3aDtNYFQRo9z9re8Cxo9dKI_'),
    'PY': ('1e4zS1wVm5umIUOShaZx0GN2M4fEgV1en', 'mic'),
    'HQ': ('1reTVn0P6iHAcTQV5GtRS3veBj_TmuF9q', 'aep')
}

def create(proj, sc, row, type_):
    name = proj.name
    if '}' in name:
        return False
    if proj.urls[URLS_MAP[sc][1]]:
        id_ = proj.urls[URLS_MAP[sc][1]]
    else:
        id_ = drive.new(name, type_, URLS_MAP[sc][0])
        proj.urls[URLS_MAP[sc][1]] = id_
        proj.save()
    set_hyperlink(sc, row, id_)
    return True

def clean(proj):
    drive.move(proj.urls[URLS_MAP['KP'][1]], URLS_MAP['KP'][2])
    drive.move(proj.urls[URLS_MAP['SJ'][1]], URLS_MAP['SJ'][2])
    drive.delete(proj.urls[URLS_MAP['PY'][1]])
    drive.delete(proj.urls[URLS_MAP['HQ'][1]])
    return True
