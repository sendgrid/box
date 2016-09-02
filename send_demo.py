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
from box_utils import get_folder
from config import CustomConfig
import sendgrid
from sendgrid.helpers.mail import *

c = CustomConfig(path=os.path.abspath(os.path.dirname(__file__)))


# Authentication
oauth = OAuth2(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    access_token=os.environ.get('DEVELOPER_TOKEN'),
)
client = Client(oauth)
root_folder = client.folder(folder_id=c.root_folder_id)

shared_folder = get_folder(client, root_folder, c.demo_folder_name)

# Grab the file from a URL and store it in Box
file = io.BytesIO(urllib.urlopen(c.file_url).read())
rn = str(int(random.random()*10000))
uploaded_file = shared_folder.upload_stream(file, '{0}_{1}.png'.format(c.file_name, rn))
shared_link = uploaded_file.get_shared_link()

# Send Email with link to file stored on Box
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(email=c.from_email, name=c.from_email_name)
subject = "SendGrid BoxDev Demo!"
to_email = Email(email=c.to_email, name=c.to_email_name)
html_content = '<html><body>Download: <a href="{}">SendGrid Logo</a></body></html>'.format(shared_link)
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
