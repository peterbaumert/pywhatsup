from pywhatsup.core.request import Request, RequestError
from pywhatsup.core.result import Entries, Entry


class Endpoint:
    def __init__(self, api, app, name, model=None):
        self.return_obj = self._lookup_ret_obj(name, model)
        self.api = api
        self.endpoint_name = name.replace("_", "-")
        self.app = app
        self._all = all
        self.url = "{base_url}/{app}/{id}/{endpoint}".format(
            base_url=self.api.base_url,
            app=self.app.app_name,
            id=self.app.id,
            endpoint=self.endpoint_name,
        )

    def _lookup_ret_obj(self, name, model):
        if model:
            name = name.title().replace("_", "")
            ret = getattr(model, name, Entry)
        else:
            ret = Entry
        return ret

    def all(self, limit=0, offset=None):
        req = Request(
            base_url=self.url,
            session=self.api.session,
            limit=limit,
            offset=offset,
            all=True,
        )
        try:
            return Entries(self, req)
        except RequestError as e:
            if e.req.status_code == 404:
                return None
            else:
                raise e

    def get(self, *args, **kwargs):
        try:
            key = args[0]
        except IndexError:
            key = None
        req = Request(
            key=key,
            base_url=self.url,
            session=self.api.session,
        )
        try:
            return next(Entries(self, req), None)
        except RequestError as e:
            if e.req.status_code == 404:
                return None
            else:
                raise e
