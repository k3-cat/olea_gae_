from . import service_drive


TYPE_MAP = {'folder': 'application/vnd.google-apps.folder',
            'doc': 'application/vnd.google-apps.document'}

def new(name, type_, root_folder_id):
    file_metadata = {
        'name': name,
        'mimeType': TYPE_MAP[type_],
        'parents': [root_folder_id]
    }
    file_ = service_drive.create(body=file_metadata,
                                 fields='id').execute()
    return file_['id']

def delete(id_):
    service_drive.update(fileId=id_,
                         body={'trashed': True},
                         fields='id').execute()
    return True

def move(id_, new_root_folder_id):
    service_drive.update(fileId=id_,
                         body={'parents': [new_root_folder_id]},
                         fields='id').execute()
    return True
