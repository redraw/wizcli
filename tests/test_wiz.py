import socket
import pytest
from unittest.mock import Mock, patch
from wizcli.wiz import Wiz

HOST = "localhost"
PORT = 1234
TIMEOUT = 5


@pytest.fixture
def wiz():
    with patch("socket.socket"):
        yield Wiz(HOST, PORT, timeout=TIMEOUT)


def test_init(wiz):
    wiz.host = HOST
    wiz.port = PORT
    wiz.socket.settimeout.assert_called_once_with(TIMEOUT)


def test_send(wiz):
    wiz.socket.recvfrom.return_value = (b'{"result": {"r": 255, "g": 0, "b": 0}}', ('', 0))
    assert wiz._send({"method": "getPilot"}) == {"result": {"r": 255, "g": 0, "b": 0}}
    wiz.socket.sendto.assert_called_once_with(b'{"method": "getPilot"}', (HOST, PORT))


def test_send_timeout(wiz):
    wiz.socket.recvfrom.side_effect = socket.timeout
    with pytest.raises(socket.timeout):
        wiz._send({"method": "getPilot"})


def test_get_state(wiz):
    wiz._send = Mock(return_value={"result": {}})
    result = wiz.get_state()
    assert result == {}
    wiz._send.assert_called_once_with({"method": "getPilot"})


def test_on(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.on()
    assert result == {"result": {"success": True}}
    wiz._send.assert_called_once_with({"method": "setPilot", "params": {"state": True}})


def test_off(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.off()
    assert result == {"result": {"success": True}}
    wiz._send.assert_called_once_with({"method": "setPilot", "params": {"state": False}})


def test_set_color(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.set_color((255, 0, 0))
    assert result == {"result": {"success": True}}
    wiz._send.assert_called_once_with({"method": "setPilot", "params": {"r": 255, "g": 0, "b": 0}})


def test_set_brightness(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.set_brightness(50)
    assert result == {"result": {"success": True}}
    wiz._send.assert_called_once_with({"method": "setPilot", "params": {"dimming": 50}})


def test_set_temp(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.set_temp(2700)
    assert result == {"result": {"success": True}}
    wiz._send.assert_called_once_with({"method": "setPilot", "params": {"temp": 2700}})


def test_set_warm(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.set_warm(50)
    assert result == {"result": {"success": True}}
    wiz._send.assert_called_once_with({"method": "setPilot", "params": {"w": 50}})


def test_set_cold(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.set_cold(50)
    assert result == {"result": {"success": True}}
    wiz._send.assert_called_once_with({"method": "setPilot", "params": {"c": 50}})


def test_push_state(wiz):
    wiz.get_state = Mock(return_value={"r": 255, "g": 0, "b": 0})
    assert len(wiz._states) == 0
    wiz.push_state()
    assert len(wiz._states) == 1
    wiz.get_state.assert_called_once()
    assert wiz._states[0] == {"r": 255, "g": 0, "b": 0}


def test_pop_state(wiz):
    wiz._states = [{"r": 255, "g": 0, "b": 0, "dimming": 50, "temp": 2700}]
    wiz._send = Mock(return_value={"result": {"success": True}})
    result = wiz.pop_state()
    wiz._send.assert_called_once_with({
        "method": "setPilot",
        "params": {"r": 255, "g": 0, "b": 0, "dimming": 50, "temp": 2700}
    })
    assert result == {"result": {"success": True}}


def test_pop_state_empty_queue(wiz):
    wiz._send = Mock(return_value={"result": {"success": True}})
    with pytest.raises(IndexError):
        wiz.pop_state()


def test_context_manager(wiz):
    with patch.object(wiz, 'push_state') as _push, patch.object(wiz, 'pop_state') as _pop:
        with wiz:
            _push.assert_called_once()
        _pop.assert_called_once()