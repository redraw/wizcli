import os
import pytest
from unittest.mock import patch
from typer.testing import CliRunner

from wizcli.cli import run

runner = CliRunner()


@pytest.fixture(autouse=True)
def wiz():
    with patch("wizcli.cli.Wiz._send", return_value={"result": {}}) as wiz_send:
        yield wiz_send


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["WIZ_HOST"] = "192.168.0.23"


def test_on():
    result = runner.invoke(run, ["on"])
    assert result.exit_code == 0


def test_off():
    result = runner.invoke(run, ["off"])
    assert result.exit_code == 0


@patch("wizcli.cli.Wiz.get_state")
def test_switch_on(mock_get_state):
    mock_get_state.return_value = {"state": False}
    result = runner.invoke(run, ["switch"])
    assert result.exit_code == 0


@patch("wizcli.cli.Wiz.get_state")
def test_switch_off(mock_get_state):
    mock_get_state.return_value = {"state": True}
    result = runner.invoke(run, ["switch"])
    assert result.exit_code == 0


def test_dim():
    result = runner.invoke(run, ["dim"])
    assert result.exit_code == 0


def test_temp():
    result = runner.invoke(run, ["temp"])
    assert result.exit_code == 0


def test_warm():
    result = runner.invoke(run, ["warm"])
    assert result.exit_code == 0


def test_cold():
    result = runner.invoke(run, ["cold"])
    assert result.exit_code == 0


def test_rgb():
    result = runner.invoke(run, ["rgb", "255", "0", "0"])
    assert result.exit_code == 0


@patch("wizcli.cli.Wiz.get_state")
def test_get(mock_get_state):
    mock_get_state.return_value = {"state": True, "r": 255, "g": 0, "b": 0}
    result = runner.invoke(run, ["get"])
    assert result.output == '{\n  "state": true,\n  "r": 255,\n  "g": 0,\n  "b": 0\n}'
    assert result.exit_code == 0


def test_missing_host():
    os.environ.pop("WIZ_HOST")
    result = runner.invoke(run, ["on"])
    assert result.exit_code == 1