from pywhatsup.models import credentials, device_groups, devices
from pywhatsup.core.endpoint import Endpoint
from pywhatsup.core.request import Request


class App(object):
    def __init__(self, api, name):
        self.api = api
        self.app_name = name
        self.id = "-"
        self.url = "{base_url}/{app}/{id}".format(
            base_url=self.api.base_url,
            app=self.app_name,
            id=self.id,
        )
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
            self.url = "{base_url}/{app}/{id}".format(
                base_url=self.api.base_url,
                app=self.app_name,
                id=self.id,
            )
            try:
                req = Request(
                    base_url=self.url,
                    session=self.api.session,
                )
                items = next(req.get())["data"].items()
                for k, v in items:
                    setattr(self, k, v)
            except:
                pass
        return self

    def __getattr__(self, name):
        return Endpoint(self.api, self, name, model=self.model)
