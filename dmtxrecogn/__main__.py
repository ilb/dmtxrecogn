from dmtxrecogn.api.controllers.recognize import recognize
from dmtxrecogn.api.controllers.heartbeat import heartbeat
from dmtxrecogn.conf import config
from bottle import Bottle
import sys
import os

if __package__ == "__main__":
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

app = Bottle()
app.default_content_type = 'application/json'


def main():
    config.init()

    app.mount("/dmtxrecogn/api/recognize", recognize)
    app.mount("/dmtxrecogn/api/heartbeat", heartbeat)
    sys.exit(
        app.run(
            server="gunicorn",
            host=config.app_host(),
            port=config.app_port(),
            debug=True,
        )
    )
