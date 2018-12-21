import os
import httplib2
from googleapiclient import discovery


CURRENT_DIR = os.path.dirname(__file__)
SCOPE = ('https://www.googleapis.com/auth/spreadsheets '
         'https://www.googleapis.com/auth/drive')

# if os.getenv('GAE_APPLICATION', None):
if True:
    from oauth2client.service_account import ServiceAccountCredentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(f'{CURRENT_DIR}/sa_cerds.json', scopes=SCOPE)
    # http = creds.authorize(httplib2.Http())

    proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080)
    http = creds.authorize(httplib2.Http(proxy_info=proxy_info, cache='R:/cache'))


service_drive = discovery.build('drive', 'v3', http=http)
service_sheet = discovery.build('sheets', 'v4', http=http).spreadsheets()
