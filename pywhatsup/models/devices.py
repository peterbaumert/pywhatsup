from pywhatsup.core.result import Entry


class Interfaces(Entry):
    pass


class Config(Entry):
    pass


class Devices(Entry):
    interfaces = Interfaces
    config = Config
