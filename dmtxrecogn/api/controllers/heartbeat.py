import logging
from logging import Logger
from bottle import Bottle, abort

logger: Logger = logging.getLogger(__name__)
heartbeat = Bottle()


@heartbeat.get()
def heartbeat(req, res):
    return "OK"
