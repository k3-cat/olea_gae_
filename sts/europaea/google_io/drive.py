from . import service_drive


TYPE_MAP = {'folder': 'application/vnd.google-apps.folder',
            'doc': 'application/vnd.google-apps.document'}

def new(root_folder_id, name, type_):
    file_metadata = {
        'name': name,
        'mimeType': TYPE_MAP[type_],
        'parents': [root_folder_id]
    }
    file_ = service_drive.files().create(body=file_metadata,
                                         fields='id').execute()
    return file_['id']

def delete(id_):
    service_drive.files().update(fileId=id_,
                                 body={'trashed': True},
                                 fields='id').execute()
    return True
