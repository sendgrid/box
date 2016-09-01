"""Receiver module for processing SendGrid Inbound Parse messages"""
import os
import io
import base64
import random

from sendgrid.helpers.inbound import Parse, Config
from boxsdk import OAuth2, Client
from flask import Flask, request

ROOT_FOLDER_ID = 0

# Configuraton
HOST = '0.0.0.0'
DEMO_FOLDER_NAME = 'BoxDev Demo Folder Incoming'
config = Config(path=os.path.abspath(os.path.dirname(__file__)))

# Authentication
oauth = OAuth2(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    access_token=os.environ.get('DEVELOPER_TOKEN'),
)
client = Client(oauth)
root_folder = client.folder(folder_id=ROOT_FOLDER_ID)


# Returns Box Folder object if exists, None otherwise
def get_folder(folder_name):
    items = client.folder(folder_id=ROOT_FOLDER_ID).get_items(limit=10, offset=0)
    folders = {}
    for item in items:
        folders[item.get()['name']] = item.get()['id']
    if folder_name in folders:
        folder_id = folders[folder_name]
        return client.folder(folder_id=folder_id).get()
    else:
        return root_folder.create_subfolder(DEMO_FOLDER_NAME)

app = Flask(__name__)


@app.route(config.endpoint, methods=['POST'])
def inbound_parse():
    parse = Parse(config, request)
    shared_folder = get_folder(DEMO_FOLDER_NAME)
    attachments = parse.attachments()
    file = io.BytesIO(base64.b64decode(attachments[2]['contents']))
    random_number = str(int(random.random()*10000))
    shared_folder.upload_stream(file, '{0}_{1}.png'.format(attachments[2]['filename'][:-4], random_number))
    # Tell SendGrid's Inbound Parse to stop sending POSTs
    # Everything is 200 OK :)
    return "OK"


if __name__ == '__main__':
    # Be sure to set config.debug_mode to False in production
    app.run(host=HOST, debug=config.debug_mode, port=config.port)