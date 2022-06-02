from pywhatsup.core.utils import Utils


class Entries(object):
    def __init__(self, endpoint, request, **kwargs):
        self.endpoint = endpoint
        self.request = request
        self.response = self.request.get()

    def __iter__(self):
        return self

    def __next__(self):
        return self.endpoint.return_obj(next(self.response))

    def __len__(self):
        try:
            return self.request.count
        except AttributeError:
            return 0


class Entry(object):
    def __init__(self, values):
        self.default_ret = Entry
        if values:
            Utils._parse_values(self, values, self.default_ret)

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
            return self.id
        else:
            return "-"

    def __hash__(self):
        return hash(self.__key__())

    def __eq__(self, other):
        if isinstance(other, Entry):
            return self.__key__() == other.__key__()
        return NotImplemented
