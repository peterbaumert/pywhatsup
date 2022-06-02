def calc_pages(limit, count):
    return int(count / limit) + (limit % count > 0)


class RequestError(Exception):
    def __init__(self, req):
        if req.status_code == 404:
            self.message = "The requested url: {} could not be found.".format(req.url)
        else:
            try:
                self.message = "The request failed with code {} {}: {}".format(
                    req.status_code, req.reason, req.json()
                )
            except ValueError:
                self.message = (
                    "The request failed with code {} {} but more specific "
                    "details were not returned in json.".format(
                        req.status_code, req.reason
                    )
                )

        super(RequestError, self).__init__(req)
        self.req = req
        self.request_body = req.request.body
        self.base = req.url
        self.error = req.text

    def __str__(self):
        return self.message


class Request(object):
    def __init__(
        self,
        base_url,
        session,
        filters=None,
        limit=None,
        offset=None,
        key=None,
        all=False,
    ):
        self.base_url = base_url
        self.filters = filters or None
        self.key = key
        self.all = all
        self.session = session
        self.url = (
            self.base_url
            if not (self.key or self.all)
            else "{base_url}/{key}".format(
                base_url=self.base_url, key=self.key if not self.all else "-"
            )
        )
        self.limit = limit
        self.offset = offset

    def get_version(self):
        req = self.session.get(
            self.base_url + "/product/api",
        )
        if data := req.json():
            return data["data"]["values"][0]["value"]
        else:
            raise Exception("Couldn't get Api Version.")

    def get(self, add_params=None):
        if not add_params and self.limit is not None:
            add_params = {"limit": self.limit}
            if self.limit and self.offset is not None:
                add_params["offset"] = self.offset
        req = self._make_call(add_params=add_params)
        if isinstance(req, dict) and req.get("paging") is not None:
            self.count = req["paging"]["size"]
            if self.offset is not None:
                for i in req["data"]:
                    yield i
            else:
                first_run = True
                for i in req["data"]:
                    if isinstance(i, dict):
                        yield i
                    else:
                        yield {i: req["data"][i]}
                while req["paging"].get("nextPageId"):
                    if first_run:
                        req = self._make_call(
                            add_params={
                                "limit": self.limit or req["paging"]["size"],
                                "offset": len(req["data"]),
                            }
                        )
                    else:
                        req = self._make_call(url_override=req["paging"]["nextPageId"])
                    first_run = False
                    for i in req["data"]:
                        yield i
        elif isinstance(req, list):
            self.count = len(req)
            for i in req:
                yield i
        else:
            self.count = len(req)
            yield req["data"]

    def _make_call(self, verb="get", url_override=None, add_params=None, data=None):
        if verb in ("post", "put") or verb == "delete" and data:
            headers = {"Content-Type": "application/json;"}
        else:
            headers = {"accept": "application/json;"}

        params = {}
        if not url_override:
            if self.filters:
                params.update(self.filters)
            if add_params:
                params.update(add_params)

        req = getattr(self.session, verb)(
            url_override or self.url, headers=headers, params=params, json=data
        )

        if verb == "delete":
            if req.ok:
                return True
            else:
                raise RequestError(req)
        elif req.ok:
            try:
                return req.json()
            except:
                raise Exception("Could not decode json data.")
        else:
            raise RequestError(req)
