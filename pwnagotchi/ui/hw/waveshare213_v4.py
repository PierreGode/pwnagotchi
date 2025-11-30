import logging
import time

import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.hw.base import DisplayImpl, DisplayInitError


class Waveshare213V4(DisplayImpl):
    """Driver wrapper for the Waveshare epd2in13_V4 panel."""

    def __init__(self, config):
        super().__init__(config, 'waveshare213_v4')
        self._display = None

    def layout(self):
        fonts.setup(10, 8, 10, 35, 25, 9)
        self._layout['width'] = 250
        self._layout['height'] = 122
        self._layout['face'] = (0, 40)
        self._layout['name'] = (5, 20)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (28, 0)
        self._layout['uptime'] = (185, 0)
        self._layout['line1'] = [0, 14, 250, 14]
        self._layout['line2'] = [0, 108, 250, 108]
        self._layout['friend_face'] = (0, 92)
        self._layout['friend_name'] = (40, 94)
        self._layout['shakes'] = (0, 109)
        self._layout['mode'] = (225, 109)
        self._layout['status'] = {
            'pos': (125, 20),
            'font': fonts.status_font(fonts.Medium),
            'max': 20
        }
        return self._layout

    def initialize(self):
        logging.info("initializing waveshare epd2in13_V4 display")
        try:
            from waveshare_epd import epd2in13_V4
        except ImportError as exc:
            logging.error(
                "waveshare_epd.epd2in13_V4 is not available; install the waveshare-epd package"
            )
            raise DisplayInitError("waveshare-epd package missing") from exc

        deadline = time.time() + 180  # allow ~3 minutes for Ragnar to release GPIOs
        attempt = 0
        last_error = None

        while time.time() < deadline:
            attempt += 1
            try:
                self._display = epd2in13_V4.EPD()
                self._display.init()
                self._display.Clear(0xFF)
                return
            except Exception as exc:
                last_error = exc
                message = str(exc)
                if 'GPIO busy' in message or 'Device or resource busy' in message:
                    logging.warning(
                        "waveshare epd2in13_V4 GPIO busy (attempt %d), waiting for display to be freed...",
                        attempt
                    )
                    time.sleep(5)
                    continue
                raise DisplayInitError("failed to initialize epd2in13_V4") from exc

        raise DisplayInitError("epd2in13_V4 display still busy after 3 minutes") from last_error

    def render(self, canvas):
        buf = self._display.getbuffer(canvas)
        self._display.displayPartial(buf)

    def clear(self):
        self._display.Clear(0xFF)
