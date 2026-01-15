"""Tests for the STB8 driver (v8_driver.py)."""
import json
from unittest.mock import AsyncMock

import pytest

from sfr_box_core.constants import CommandType
from sfr_box_core.constants import KeyCode
from sfr_box_core.v8_driver import V8Driver
from sfr_box_core.v8_driver import _STB8CommandBuilder


@pytest.fixture
def v8_driver():
    """Provides a V8Driver instance with a mocked send_message."""
    driver = V8Driver(host="localhost", port=8080, device_id="test-stb8")
    driver.send_message = AsyncMock()  # Mock the parent's send_message
    return driver


@pytest.mark.asyncio
async def test_stb8_command_builder_send_key():
    """Test building a SEND_KEY payload."""
    builder = _STB8CommandBuilder(device_id="test-stb8")
    payload = builder.build_send_key(KeyCode.POWER)
    assert payload is not None
    parsed_payload = json.loads(payload)

    assert parsed_payload["action"] == "buttonEvent"
    assert parsed_payload["deviceId"] == "test-stb8"
    assert "requestId" in parsed_payload
    assert parsed_payload["params"]["key"] == "power"


@pytest.mark.asyncio
async def test_stb8_command_builder_get_status():
    """Test building a GET_STATUS payload."""
    builder = _STB8CommandBuilder(device_id="test-stb8")
    payload = builder.build_get_status()
    assert payload is not None
    parsed_payload = json.loads(payload)

    assert parsed_payload["action"] == "getStatus"
    assert parsed_payload["deviceId"] == "test-stb8"
    assert "requestId" in parsed_payload
    assert "params" not in parsed_payload  # No params for getStatus


@pytest.mark.asyncio
async def test_stb8_command_builder_get_versions():
    """Test building a GET_VERSIONS payload."""
    builder = _STB8CommandBuilder(device_id="test-stb8")
    payload = builder.build_get_versions(device_name="my-device")
    assert payload is not None
    parsed_payload = json.loads(payload)

    assert parsed_payload["action"] == "getVersions"
    assert parsed_payload["deviceId"] == "test-stb8"
    assert "requestId" in parsed_payload
    assert parsed_payload["params"]["deviceName"] == "my-device"


@pytest.mark.asyncio
async def test_v8_driver_send_key(v8_driver):
    """Test V8Driver's send_command with SEND_KEY."""
    await v8_driver.send_command(CommandType.SEND_KEY, key=KeyCode.HOME)
    v8_driver.send_message.assert_awaited_once()
    sent_payload = json.loads(v8_driver.send_message.call_args[0][0])
    assert sent_payload["action"] == "buttonEvent"
    assert sent_payload["params"]["key"] == "home"


@pytest.mark.asyncio
async def test_v8_driver_get_status(v8_driver):
    """Test V8Driver's send_command with GET_STATUS."""
    await v8_driver.send_command(CommandType.GET_STATUS)
    v8_driver.send_message.assert_awaited_once()
    sent_payload = json.loads(v8_driver.send_message.call_args[0][0])
    assert sent_payload["action"] == "getStatus"
    assert "params" not in sent_payload


@pytest.mark.asyncio
async def test_v8_driver_get_versions(v8_driver):
    """Test V8Driver's send_command with GET_VERSIONS."""
    # The device_id is passed during driver init and used for deviceName
    await v8_driver.send_command(CommandType.GET_VERSIONS)
    v8_driver.send_message.assert_awaited_once()
    sent_payload = json.loads(v8_driver.send_message.call_args[0][0])
    assert sent_payload["action"] == "getVersions"
    assert sent_payload["params"]["deviceName"] == "test-stb8"
