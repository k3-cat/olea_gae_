import os
import httplib2
from googleapiclient import discovery


CURRENT_DIR = os.path.dirname(__file__)

if os.getenv('GAE_APPLICATION', None):
    from oauth2client import file, client, tools
    store = file.Storage(f'{CURRENT_DIR}/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(f'{CURRENT_DIR}/creds.json',
                                              scope='https://www.googleapis.com/auth/spreadsheets '
                                                    'https://www.googleapis.com/auth/drive')
        creds = tools.run_flow(flow, store)
    http = creds.authorize(httplib2.Http())
else:
    from oauth2client import file, client, tools
    store = file.Storage(f'{CURRENT_DIR}/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(f'{CURRENT_DIR}/creds.json',
                                              scope='https://www.googleapis.com/auth/spreadsheets '
                                                    'https://www.googleapis.com/auth/drive')
        creds = tools.run_flow(flow, store)
    proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080)
    http = creds.authorize(httplib2.Http(proxy_info=proxy_info, cache='R:/cache'))


service_drive = discovery.build('drive', 'v3', http=http)
service_sheet = discovery.build('sheets', 'v4', http=http).spreadsheets()
