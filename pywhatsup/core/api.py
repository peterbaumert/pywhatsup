import requests
from pywhatsup.core.app import App
from pywhatsup.core.request import Request


class Api(object):
    def __init__(self, url, username=None, password=None):
        self.username = username
        self.password = password
        self.token = ""
        self.base_url = "{}/api/v1".format(url if url[-1] != "/" else url[:-1])
        self.session = requests.Session()
        self.session.verify = False
        self.login()
        self.credentials = App(self, "credentials")
        self.devices = App(self, "devices")
        self.device_groups = App(self, "device_groups")
        self.monitors = App(self, "monitors")

    def login(self):
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }
        r = self.session.post(
            url=self.base_url + "/token",
            data=data,
        )
        if r.status_code != 200:
            raise Exception("Login Error")

        self.session.headers = {"Authorization": "Bearer " + r.json()["access_token"]}

    @property
    def version(self):
        version = Request(
            base_url=self.base_url,
            session=self.session,
        ).get_version()
        return version
