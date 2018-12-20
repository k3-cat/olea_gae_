from . import service_sheet


class Path:
    def __init__(self, id_=None, table=None):
        self.id_ = id_
        self.table = table
        self.col_ = ('', '')
        self.row_ = ('', '')

    @property
    def col(self):
        return ':'.join(self.col_)

    @property
    def row(self):
        return ':'.join(self.row_)

    @col.setter
    def col(self, col):
        if ':' in col:
            self.col_ = col.split(':')
        else:
            self.col_ = (col, col)

    @row.setter
    def row(self, row):
        if ':' in row:
            self.row_ = row.split(':')
        else:
            self.row_ = (row, row)

    @property
    def range(self):
        return f'{self.table}!{self.col_[0]}{self.row_[0]}:{self.col_[1]}{self.row_[1]}'

    @property
    def sheet_id(self):
        sheet_metadata = service_sheet.get(spreadsheetId=self.id_,
                                           fields='sheets/properties/title,'
                                                  'sheets/properties/sheetId').execute()
        for table in sheet_metadata['sheets']:
            if table['properties']['title'] == self.table:
                return table['properties']['sheetId']
        return None


def get_values(path):
    request = service_sheet.values().get(spreadsheetId=path.id_, range=path.range)
    return request.execute()['values']

def set_values(path, value, row_from=True):
    body = {'values': value}
    if row_from:
        body['majorDimension'] = 'ROWS'
    else:
        body['majorDimension'] = 'COLUMNS'
    request = service_sheet.values().update(
        spreadsheetId=path.id_,
        range=path.range,
        valueInputOption='RAW',
        body=body)
    return request.execute()

def append(path, value, row_from=True):
    body = {'values': value}
    if row_from:
        body['majorDimension'] = 'ROWS'
    else:
        body['majorDimension'] = 'COLUMNS'
    request = service_sheet.values().append(
        spreadsheetId=path.id_,
        range=path.range,
        valueInputOption='RAW',
        body=body)
    return request.execute()

def del_line(path):
    body = {'requests': [
        {'deleteDimension': {
            'range': {
                'sheetId': path.sheet_id,
                'dimension': 'ROWS',
                'startIndex': str(int(path.row_[0])-1),
                'endIndex': path.row_[1]}}}
    ]}
    service_sheet.batchUpdate(spreadsheetId=path.id_, body=body).execute()
    return True

def countrow_s(path):
    sheet_metadata = service_sheet.get(spreadsheetId=path.id_,
                                       fields='sheets/properties/title,'
                                              'sheets/properties/gridProperties/rowCount').execute()
    for table in sheet_metadata['sheets']:
        if table['properties']['title'] == path.table:
            return table['properties']['gridProperties']['rowCount']
    return None

TABLES_NAME = dict()

def list_tables(path):
    id_ = path.id_
    if id_ not in TABLES_NAME.keys():
        sheet_metadata = service_sheet.get(spreadsheetId=id_,
                                           fields='sheets/properties/title').execute()
        tables = list()
        for table in sheet_metadata['sheets']:
            tables.append(table['properties']['title'])
        TABLES_NAME[id_] = tables
        TABLES_NAME[id_].sort()
    return TABLES_NAME[id_]
