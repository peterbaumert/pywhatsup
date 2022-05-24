from pywhatsup.models import credentials, device_groups, devices
from pywhatsup.core.endpoint import Endpoint


class App(object):
    def __init__(self, api, name):
        self.api = api
        self.app_name = name
        self._setmodel()

    models = {
        "credentials": credentials,
        "devices": devices,
        "device_groups": device_groups,
    }

    def _setmodel(self):
        self.model = App.models[self.app_name] if self.app_name in App.models else None

    def __getstate__(self):
        return {"api": self.api, "name": self.app_name}

    def __setstate__(self, d):
        self.__dict__.update(d)
        self._setmodel()

    def __call__(self, *args, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        return self

    def __getattr__(self, name):
        return Endpoint(self.api, self, name, model=self.model)
