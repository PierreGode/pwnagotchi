import _thread
import secrets
import logging
import os
import time

# https://stackoverflow.com/questions/14888799/disable-console-messages-in-flask-server
logging.getLogger('werkzeug').setLevel(logging.ERROR)

from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from werkzeug.serving import make_server

from pwnagotchi.ui.web.handler import Handler

class Server:
    def __init__(self, agent, config):
        self._config = config['web']
        self._enabled = self._config['enabled']
        self._port = self._config['port']
        self._address = self._config['address']
        self._origin = None
        self._agent = agent
        if 'origin' in self._config:
            self._origin = self._config['origin']

        if self._enabled:
            _thread.start_new_thread(self._http_serve, ())

    def _http_serve(self):
        if self._address is not None:
            web_path = os.path.dirname(os.path.realpath(__file__))

            app = Flask(__name__,
                        static_url_path='',
                        static_folder=os.path.join(web_path, 'static'),
                        template_folder=os.path.join(web_path, 'templates'))

            app.secret_key = secrets.token_urlsafe(256)

            if self._origin:
                CORS(app, resources={r"*": {"origins": self._origin}})

            CSRFProtect(app)
            Handler(self._config, self._agent, app)

            logging.info("web ui available at http://%s:%d/" % (self._address, self._port))

            deadline = time.time() + 180  # give Ragnar time to free port 8000
            attempt = 0
            server = None

            while time.time() < deadline:
                attempt += 1
                try:
                    server = make_server(self._address, self._port, app, threaded=True)
                    break
                except OSError as exc:
                    logging.warning(
                        "web ui port %d busy (attempt %d): %s; retrying...",
                        self._port,
                        attempt,
                        exc
                    )
                    time.sleep(5)

            if server is None:
                logging.error("web ui failed to bind %s:%d after 3 minutes; disabling web UI", self._address, self._port)
                return

            server.serve_forever()
        else:
            logging.info("could not get ip of usb0, video server not starting")
