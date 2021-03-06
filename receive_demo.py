import base64
import os
import io
import random

from config import CustomConfig
from boxsdk import OAuth2, Client
from box_utils import get_folder
from flask import Flask, request, render_template
from sendgrid.helpers.inbound import Parse

c = CustomConfig(path=os.path.abspath(os.path.dirname(__file__)))


# Authentication
oauth = OAuth2(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    access_token=os.environ.get('DEVELOPER_TOKEN'),
)
client = Client(oauth)
root_folder = client.folder(folder_id=c.root_folder_id)

application = Flask(__name__)


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@application.route(c.endpoint, methods=['POST'])
def inbound_parse():
    parse = Parse(c, request)
    shared_folder = get_folder(client, root_folder, c.demo_folder_name_incoming)

    # Parse the attachments
    attachments = parse.attachments()
    file = io.BytesIO(base64.b64decode(attachments[0]['contents']))
    random_number = str(int(random.random()*10000))
    suffix = attachments[0]['file_name'][-4:]
    file_name = '{0}_{1}.{2}'.format(attachments[0]['file_name'][:-4], random_number, suffix)

    # Store the attachment in Box
    shared_folder.upload_stream(file, file_name, random_number)

    # Tell SendGrid's Inbound Parse to stop sending POSTs
    # Everything is 200 OK :)
    return "OK"


if __name__ == '__main__':
    # Be sure to set config.debug_mode to False in production

    if os.environ.get('AWS') == 'False':
        application.host = c.flask_host
        application.port = c.port
        application.debug = c.debug_mode
    else:
        application.debug = False

    application.run()
