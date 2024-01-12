from functools import lru_cache
from os.path import dirname, realpath

from pycontext import shared_context

def init() -> None:
    shared_context.init(dirname(realpath(__file__)) + "/web.xml")


@lru_cache(1)
def app_port():
    return shared_context.get("apps.dmtxrecogn.port")


@lru_cache(1)
def app_host():
    return shared_context.get("apps.dmtxrecogn.host")

