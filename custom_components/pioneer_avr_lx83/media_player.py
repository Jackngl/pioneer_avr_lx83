"""Support for Pioneer AVR LX83 receivers."""
from __future__ import annotations

import logging
import telnetlib
from typing import Any

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CMD_MUTE_OFF,
    CMD_MUTE_ON,
    CMD_MUTE_QUERY,
    CMD_POWER_OFF,
    CMD_POWER_ON,
    CMD_POWER_QUERY,
    CMD_SOURCE,
    CMD_SOURCE_QUERY,
    CMD_VOLUME,
    CMD_VOLUME_QUERY,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SOURCES,
    DEFAULT_TIMEOUT,
    DOMAIN,
    SUPPORT_PIONEER,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pioneer AVR LX83 media player."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data.get(CONF_PORT, DEFAULT_PORT)
    name = config_entry.data.get(CONF_NAME, DEFAULT_NAME)

    async_add_entities([PioneerAVR(hass, name, host, port)], True)


class PioneerAVR(MediaPlayerEntity):
    """Representation of a Pioneer AVR LX83."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_icon = "mdi:amplifier"

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        host: str,
        port: int,
    ) -> None:
        """Initialize the Pioneer AVR device."""
        self.hass = hass
        self._attr_unique_id = f"pioneer_telnet_{host}_{port}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": name,
            "manufacturer": "Pioneer",
            "model": "AVR LX83",
        }
        self._host = host
        self._port = port
        self._name = name
        self._state = STATE_OFF
        self._volume = 0.0
        self._is_muted = False
        self._source = None
        self._sources = DEFAULT_SOURCES
        self._available = True

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return self._name

    @property
    def state(self) -> str:
        """Return the state of the device."""
        return self._state

    @property
    def volume_level(self) -> float:
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def is_volume_muted(self) -> bool:
        """Boolean if volume is currently muted."""
        return self._is_muted

    @property
    def source(self) -> str | None:
        """Return the current input source."""
        return self._source

    @property
    def source_list(self) -> list[str]:
        """List of available input sources."""
        return list(self._sources.keys())

    @property
    def supported_features(self) -> int:
        """Flag media player features that are supported."""
        return SUPPORT_PIONEER

    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return self._available

    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        await self._send_command(CMD_POWER_ON)
        self._state = STATE_ON
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn off media player."""
        await self._send_command(CMD_POWER_OFF)
        self._state = STATE_OFF
        self.async_write_ha_state()

    async def async_volume_up(self) -> None:
        """Volume up media player."""
        if self._volume < 1.0:
            new_volume = min(self._volume + 0.01, 1.0)
            await self.async_set_volume_level(new_volume)

    async def async_volume_down(self) -> None:
        """Volume down media player."""
        if self._volume > 0.0:
            new_volume = max(self._volume - 0.01, 0.0)
            await self.async_set_volume_level(new_volume)

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        volume_int = int(volume * 185)
        await self._send_command(f"{CMD_VOLUME}{volume_int:03d}")
        self._volume = volume
        self.async_write_ha_state()

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute (true) or unmute (false) media player."""
        if mute:
            await self._send_command(CMD_MUTE_ON)
        else:
            await self._send_command(CMD_MUTE_OFF)
        self._is_muted = mute
        self.async_write_ha_state()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        if source in self._sources:
            source_code = self._sources[source]
            await self._send_command(f"{CMD_SOURCE}{source_code}")
            self._source = source
            self.async_write_ha_state()

    async def async_update(self) -> None:
        """Get the latest details from the device."""
        try:
            # Query power state
            power_response = await self._send_command_with_response(CMD_POWER_QUERY)
            if power_response:
                self._state = STATE_ON if b"PWR0" in power_response else STATE_OFF
                self._available = True
            else:
                self._available = False
                return

            if self._state == STATE_ON:
                # Query volume
                volume_response = await self._send_command_with_response(CMD_VOLUME_QUERY)
                if volume_response and b"VOL" in volume_response:
                    try:
                        vol_str = volume_response.decode().strip()
                        vol_value = int(vol_str.replace("VOL", ""))
                        self._volume = vol_value / 185.0
                    except (ValueError, AttributeError):
                        pass

                # Query mute state
                mute_response = await self._send_command_with_response(CMD_MUTE_QUERY)
                if mute_response:
                    self._is_muted = b"MUT0" in mute_response

                # Query source
                source_response = await self._send_command_with_response(CMD_SOURCE_QUERY)
                if source_response and b"FN" in source_response:
                    try:
                        src_str = source_response.decode().strip()
                        src_code = src_str.replace("FN", "")
                        for name, code in self._sources.items():
                            if code == src_code:
                                self._source = name
                                break
                    except (ValueError, AttributeError):
                        pass

        except Exception as err:
            _LOGGER.error("Error updating Pioneer AVR: %s", err)
            self._available = False

    async def _send_command(self, command: str) -> None:
        """Send a command to the Pioneer AVR."""
        try:
            await self.hass.async_add_executor_job(
                self._send_command_sync, command
            )
        except Exception as err:
            _LOGGER.error("Error sending command '%s': %s", command, err)
            self._available = False

    async def _send_command_with_response(self, command: str) -> bytes | None:
        """Send a command and get response."""
        try:
            return await self.hass.async_add_executor_job(
                self._send_command_sync_with_response, command
            )
        except Exception as err:
            _LOGGER.error("Error sending command '%s': %s", command, err)
            self._available = False
            return None

    def _send_command_sync(self, command: str) -> None:
        """Send command synchronously."""
        with telnetlib.Telnet(self._host, self._port, timeout=DEFAULT_TIMEOUT) as tn:
            tn.write(command.encode() + b"\r\n")

    def _send_command_sync_with_response(self, command: str) -> bytes:
        """Send command and get response synchronously."""
        with telnetlib.Telnet(self._host, self._port, timeout=DEFAULT_TIMEOUT) as tn:
            tn.write(command.encode() + b"\r\n")
            return tn.read_until(b"\r\n", timeout=DEFAULT_TIMEOUT)