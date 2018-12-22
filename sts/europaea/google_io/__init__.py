import os
import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


CURRENT_DIR = os.path.dirname(__file__)
SCOPES = ('https://www.googleapis.com/auth/spreadsheets '
         'https://www.googleapis.com/auth/drive')
SA_CREDS = {
  "type": "service_account",
  "project_id": "olea-0",
  "private_key_id": "ac4ec9e17ce8e3076410f93fb3b47ac3ccd70fcc",
  "private_key": """-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqW8VQ4qGx9AE4\nkMZPBsbNgydreqHp/joLlQ2ytiUWMQzg8dFGRbmJvYcK0VRaF0BSkjBqIXG9+TeT\n0eOrwgdRiy8ipADxfgaMxm6b7mRi8yxZ/Vpo5g60bzTB6vCT7yC6gy6q8A6SWexb\n10aBb1LkLZ226Q1scLTmJLW3+AJj8lfqGLTFy8IMZp1O8u8q/nfRUzP8ybU+AotS\nqvgPRmDIG0yQWhL3jNwx6QAxYLNkpAodDa6YFR4J7PrGk1dzVd9to4Y4SkPQcY35\n6khNNHy8ddeQSyg8cmmkEh1GvwqZtu+nVAvzGf0LEjeEi/gF17rOIzPfEmFu1PLD\ne1EzW7/ZAgMBAAECggEADNk/0ixLp3soqepiaJSxYw/qpdSxmE8+M8At0K4j8S7p\nIqCeaPNKjXjT0fUsjGBvT6L6v5Bu7pX4sv+MMTjAuk3Z894Ee7JGfnDbaAuUevGO\nBWoCOwHp90Iha6RDeZbaJDMPbqFNKgzZ8qnThaDesrq9h81/P4/nFuoLIhlUndLK\ndmFsFLEHbi4JYq9do72ui7za23RBdcHDZxBuR0nYapp58+VN0yszwrpgG/9B9Ctv\n1/djOOs+bd372uZzZAb9udb1jQJ+eU9fVa7cjQaI5cyRqXmk5zo3SWZujkcyEiAi\nBXPCtJ8HQvvid1c4WVmIgy1IQWjmKx2b3WVancXDUQKBgQDaIXmluXDT8YmCcgf6\nB49VCrvSTYlsSbDFQkuE/7ACtQbI3hvSDJBuYCr6AxZ2dlmt8ve7qRbBvpsbYgm+\nBPRxuouTTtq1ZudCYicJETRgA59v6XfXODalF/sUAxUNQemU8daKy+hJdmS3pu54\nKX1gwwFLYbEIgX3uPZRanMLX8QKBgQDH7x8aVT1osrStmMrN0q4/pbcXtcIRCBeh\nFKXXsZyB05AqDSnHKDCEBAMVePK7YlKRfS4X8uLd8vRnKGQ3b5dCZcPxIGxdkDrp\nFqyy8wwgGNrIhpoD5hqbfWOlGD/h96WSGIVWGCs9dMeHA6PfekP4zn0PAaKnFiZ/\nDjg5S8IOaQKBgQCyZZRW3I4RWMaMv/QUIeCwvaGUwsM0pCQFgE3BTVhHLoSI/VYl\neQ8apl4fsSzK38pCgKbpfMXW2KuEPq8XEHhXFykV5fTrTWivmxSvzrlWGUBpR7ky\ndJAEf9Nhr4+lExYVMaC0TUYB5ulCZi08azpWS8YgP5qJCVbT5NsTLIgSEQKBgG0l\n6/LySf4YYW7MFRtcQuhYTaZSAcpOgqfbn9YrDmgJ2ZA7c21YUXQgxJY6WzlVKgJn\nNny4ioXkluyiLmPdNdR3vgqrSr2heae6Szm+WgZDy1zhrr8mJaxxPa7pmCaCjg89\n97zSoPiCAlOA9zuPggAYqklA+U0CWK3QU31kEGLRAoGAOgcdSXwspBklqw5DLWMV\nRGYH7kh7t8o3Xx4zoiQGqqSxcvUJFKJw7qd04t9JvFGpXhTBoNjJJsw8v1n7yrX4\nnqlSPEDAuJLXkVfeF+P7FAUCnN+3sn63EjNGq7awY3T1rxzBjr+yNTjhnZJqBYdA\n9yCAMlexSQF2fnfdEZty+4k=\n-----END PRIVATE KEY-----\n""",
  "client_email": "olea-0@appspot.gserviceaccount.com",
  "client_id": "114286707588855606515",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/olea-0%40appspot.gserviceaccount.com"
}


creds = ServiceAccountCredentials.from_json_keyfile_dict(SA_CREDS, scopes=SCOPES)
if os.getenv('GAE_APPLICATION', None):
    http = creds.authorize(httplib2.Http())
else:
    proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080)
    http = creds.authorize(httplib2.Http(proxy_info=proxy_info, cache='R:/cache'))


service_drive = discovery.build('drive', 'v3', http=http)
service_sheets = discovery.build('sheets', 'v4', http=http).spreadsheets()
