"""Support for Pioneer AVR LX83 receivers."""
from __future__ import annotations

import logging
import telnetlib
from typing import Any
from datetime import timedelta

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

# Supprimez cette ligne qui cause l'erreur
# SCAN_INTERVAL = 10  # seconds
# Utilisez plutôt la constante SCAN_INTERVAL importée de const.py


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

    # Le reste du code reste inchangé