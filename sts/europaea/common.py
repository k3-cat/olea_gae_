from .global_value import HL_MAP, PATH_MAP
from .google_io import sheets


def get_path(code):
    return sheets.Path(id_=PATH_MAP[code][0], table=PATH_MAP[code][1])


def hyperlink(url_, type_):
    if not url_:
        return ''
    if '{' in url_:
        return url_
    return f'=HYPERLINK("{HL_MAP[type_][0]}{url_}","[{HL_MAP[type_][1]*4}]")'
