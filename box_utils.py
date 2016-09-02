import os
from config import CustomConfig

c = CustomConfig(path=os.path.abspath(os.path.dirname(__file__)))

# Returns Box Folder object if exists, None otherwise
def get_folder(client, root_folder, folder_name):
    items = client.folder(folder_id=c.root_folder_id).get_items(limit=10, offset=0)
    folders = {}
    for item in items:
        folders[item.get()['name']] = item.get()['id']
    if folder_name in folders:
        folder_id = folders[folder_name]
        return client.folder(folder_id=folder_id).get()
    else:
        return root_folder.create_subfolder(folder_name)