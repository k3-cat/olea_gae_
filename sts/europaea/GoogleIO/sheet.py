from . import service_sheet


class Path:
    def __init__(self, id_=None, table=None):
        self.id_ = id_
        self.table = table
        self._col = ('', '')
        self._row = ('', '')

    @property
    def col(self):
        return ':'.join(self._col)

    @property
    def row(self):
        return ':'.join(self._row)

    @col.setter
    def col(self, col):
        if ':' in col:
            self._col = col.split(':')
        else:
            self._col = (col, col)

    @row.setter
    def row(self, row):
        if ':' in row:
            self._row = row.split(':')
        else:
            self._row = (row, row)

    @property
    def range(self):
        return f'{self.table}!{self._col[0]}{self._row[0]}:{self._col[1]}{self._row[1]}'

    @property
    def sheet_id(self):
        for table in service_sheet.get(spreadsheetId=self.id_,
                                       fields='properties/title,'
                                              'properties/sheetId').execute():
            if table['properties']['title'] == table:
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
                'startIndex': path.row[0],
                'endIndex': path.row[1]}}}
    ]}
    service_sheet.batchUpdate(spreadsheetId=path.id_, body=body).execute()
    return True

def count_rows(path):
    sheet_metadata = service_sheet.get(spreadsheetId=path.id_).execute()
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
