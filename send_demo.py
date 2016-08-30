import os
import io
import random
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib
from boxsdk import OAuth2, Client
import sendgrid
from sendgrid.helpers.mail import *

ROOT_FOLDER_ID = 0
DEMO_FOLDER_NAME = 'BoxDev Demo Folder'
DEMO_FOLDER_ID = None
FILE_URL = 'https://sendgrid.com/wp-content/themes/sgdotcom/pages/brand/2016/SendGrid-Logo.png'

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

shared_folder = get_folder(DEMO_FOLDER_NAME)

# Grab the file from a URL and store it in Box
file = io.BytesIO(urllib.urlopen(FILE_URL).read())
uploaded_file = shared_folder.upload_stream(file, 'SendGrid_Logo_' + str(int(random.random()*10000)) + '.png')
shared_link = uploaded_file.get_shared_link()

# Send Email with link to file stored on Box
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(email="dx@sendgrid.com", name="DX Team")
subject = "SendGrid BoxDev Demo!"
to_email = Email(email="elmer.thomas@sendgrid.com", name="Elmer Thomas")
html_content = '<html><body>Download Here: <a href="{}">SendGrid Logo File</a></body></html>'.format(shared_link)
content = Content(type="text/html", value=html_content)
mail = Mail(from_email=from_email, subject=subject, to_email=to_email, content=content)
try:
    response = sg.client.mail.send.post(request_body=mail.get())
except urllib.HTTPError as e:
    print(e.read())

if response.status_code == 202:
    print("Check your Inbox!")
else:
    print("Demo Failed :(")
