import os
import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


CURRENT_DIR = os.path.dirname(__file__)
SCOPE = ('https://www.googleapis.com/auth/spreadsheets '
         'https://www.googleapis.com/auth/drive')

creds = ServiceAccountCredentials.from_json_keyfile_name(
    f'{os.path.dirname(__file__)}/../sa_creds.json',
    scopes=SCOPE)
if os.getenv('GAE_APPLICATION', None):
    http = creds.authorize(httplib2.Http())
else:
    proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080)
    http = creds.authorize(httplib2.Http(proxy_info=proxy_info, cache='R:/cache'))


service_drive = discovery.build('drive', 'v3', http=http)
service_sheets = discovery.build('sheets', 'v4', http=http).spreadsheets()
