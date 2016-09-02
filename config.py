from sendgrid.helpers.inbound import Parse, Config
import os
import yaml


class CustomConfig(Config):
    def __init__(self, **opts):
        super(CustomConfig, self).__init__(**opts)
        self.path = opts.get('path', os.path.abspath(os.path.dirname(__file__)))
        with open(self.path + '/config.yml') as stream:
            config = yaml.load(stream)
            self._root_folder_id = config['root_folder_id']
            self._flask_host = config['flask_host']
            self._demo_folder_name_incoming = config['demo_folder_name_incoming']
            self._demo_folder_name = config['demo_folder_name']
            self._demo_folder_id = config['demo_folder_id']
            self._file_url = config['file_url']
            self._file_name = config['file_name']
            self._from_email = config['from_email']
            self._from_email_name = config['from_email_name']
            self._to_email = config['to_email']
            self._to_email_name = config['to_email_name']

    @property
    def root_folder_id(self):
        return self._root_folder_id

    @property
    def flask_host(self):
        return self._flask_host

    @property
    def demo_folder_name_incoming(self):
        return self._demo_folder_name_incoming

    @property
    def demo_folder_name(self):
        return self._demo_folder_name

    @property
    def demo_folder_id(self):
        return self._demo_folder_id

    @property
    def file_url(self):
        return self._file_url

    @property
    def file_name(self):
        return self._file_name

    @property
    def from_email(self):
        return self._from_email

    @property
    def from_email_name(self):
        return self._from_email_name

    @property
    def to_email(self):
        return self._to_email

    @property
    def to_email_name(self):
        return self._to_email_name
