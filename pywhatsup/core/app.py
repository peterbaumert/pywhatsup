from pywhatsup.core.result import Entries, Entry
from pywhatsup.core.utils import Utils
from pywhatsup.models import credentials, device_groups, devices, monitors
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
        self.return_obj = self._lookup_ret_obj(name, self.model)

    def _lookup_ret_obj(self, name, model):
        if model:
            name = name.title().replace("_", "")
            ret = getattr(model, name, Entry)
        else:
            ret = Entry
        return ret

    models = {
        "credentials": credentials,
        "devices": devices,
        "device_groups": device_groups,
        "monitors": monitors,
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
            # if self.id == "-":
            entries = req.get()
            for entry in entries:
                Utils._parse_values(self, entry, Entry)
        except:
            pass
        return self

    def __getattr__(self, name):
        return Endpoint(self.api, self, name, model=self.model)
