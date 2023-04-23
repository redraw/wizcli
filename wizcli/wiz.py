import json
import socket
import logging
from pprint import pformat
from collections import deque

logger = logging.getLogger(__name__)


class Wiz:
    STATE_FIELDS = ("r", "g", "b", "c", "w", "dimming", "temp")

    def __init__(self, host: str, port: int = 38899, timeout: int = 5):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)
        self._states = deque()

    def __enter__(self):
        self.push_state()
        return self

    def __exit__(self, *args, **kwargs):
        logger.info("Restoring WiZ state...")
        self.pop_state()

    def _send(self, payload: dict) -> dict:
        body = json.dumps(payload)
        addr = (self.host, self.port)

        logger.debug(f" > {pformat(payload)}")
        self.socket.sendto(body.encode("utf8"), addr)

        try:
            content, _ = self.socket.recvfrom(4096)
            response = json.loads(content)
            logger.debug(f" < {pformat(response)}")

            return response
        except socket.timeout as e:
            logger.error("wiz bulb timeout")
            raise e

    def get_state(self) -> dict:
        return self._send({"method": "getPilot"}).get("result")

    def on(self):
        return self._send({"method": "setPilot", "params": {"state": True}})

    def off(self):
        return self._send({"method": "setPilot", "params": {"state": False}})

    def set_color(self, rgb):
        r, g, b = rgb
        return self._send({"method": "setPilot", "params": {"r": r, "g": g, "b": b}})

    def set_brightness(self, value):
        return self._send({"method": "setPilot", "params": {"dimming": value}})

    def set_temp(self, value):
        return self._send({"method": "setPilot", "params": {"temp": value}})

    def set_warm(self, value):
        return self._send({"method": "setPilot", "params": {"w": value}})

    def set_cold(self, value):
        return self._send({"method": "setPilot", "params": {"c": value}})

    def push_state(self):
        """push state to the queue"""
        state = self.get_state()
        self._states.append(state)

    def pop_state(self):
        state = self._states.pop()
        return self._send({
            "method": "setPilot",
            "params": {k: v for k, v in state.items() if k in self.STATE_FIELDS}
        })
