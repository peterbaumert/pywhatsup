import copy


class Entries(object):
    def __init__(self, endpoint, request, **kwargs):
        self.endpoint = endpoint
        self.request = request
        self.response = self.request.get()

    def __iter__(self):
        return self

    def __next__(self):
        return self.endpoint.return_obj(
            next(self.response), self.endpoint.api, self.endpoint
        )

    def __len__(self):
        try:
            return self.request.count
        except AttributeError:
            return 0


class Entry(object):
    def __init__(self, values, api, endpoint):
        self.api = api
        self.endpoint = endpoint
        self.default_ret = Entry
        if values:
            self._parse_values(values)

    def _getattr__(self, k):
        raise AttributeError('object has no attribute "{}"'.format(k))

    def __getitem__(self, k):
        return dict(self)[k]

    def __str__(self):
        return getattr(self, "name", None) or getattr(self, "hostName", None) or ""

    def __repr__(self):
        return str(self)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __key__(self):
        if hasattr(self, "id"):
            return (self.endpoint.endpoint_name, self.id)
        else:
            return self.endpoint.endpoint_name

    def __hash__(self):
        return hash(self.__key__())

    def __eq__(self, other):
        if isinstance(other, Entry):
            return self.__key__() == other.__key__()
        return NotImplemented

    def _parse_values(self, values):
        def list_parser(key_name, list_item):
            if isinstance(list_item, dict):
                lookup = getattr(self.__class__, key_name, None)
                if not isinstance(lookup, list):
                    return self.default_ret(list_item, self.api, self.endpoint)
                else:
                    model = lookup[0]
                    return model(list_item, self.api, self.endpoint)
            return list_item

        items = values["data"].items() if values.get("data") else values.items()

        for k, v in items:
            if isinstance(v, dict):
                lookup = getattr(self.__class__, k, None)
                if lookup:
                    v = lookup(v, self.api, self.endpoint)
                else:
                    v = self.default_ret(v, self.api, self.endpoint)

            elif isinstance(v, list):
                v = [list_parser(k, i) for i in v]

            setattr(self, k, v)
