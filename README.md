# pywhatsup
![PyPI - Downloads](https://img.shields.io/pypi/dm/pywhatsup) ![GitHub](https://img.shields.io/github/license/peterbaumert/pywhatsup) ![PyPI](https://img.shields.io/pypi/v/pywhatsup)

Still work in progress :)

## usage
```
from pywhatsup import api

whatsup = api("https://whats.up.gold:9644", "user", "password")

dev = whatsup.devices(id=422)
interfaces = dev.interfaces.all()
int = dev.interfaces.get("1502")
poll = dev.config.get("polling")
```
