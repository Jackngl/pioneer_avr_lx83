"""The Pioneer AVR LX83 integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .services import async_setup_services, async_unload_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.MEDIA_PLAYER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pioneer AVR LX83 from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Set up services
    await async_setup_services(hass)

    # Utiliser async_create_task pour éviter les appels bloquants
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )

    # Register the entity for Alexa discovery
    async def async_alexa_discovery(hass, config_entry, alexa_config):
        """Handle Alexa discovery requests."""
        from .alexa import PioneerAVRAlexaEntity
        
        media_players = hass.data.get("media_player", {}).get(DOMAIN, [])
        entities = []
        
        for media_player in media_players:
            entities.append(PioneerAVRAlexaEntity(media_player))
            
        return entities
    
    # Register the discovery function with Home Assistant
    if "alexa" in hass.config.components:
        hass.data.setdefault("alexa", {})
        hass.data["alexa"].setdefault("entities", {})
        hass.data["alexa"]["entities"][DOMAIN] = async_alexa_discovery

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Remove from Alexa discovery
        if "alexa" in hass.config.components and DOMAIN in hass.data.get("alexa", {}).get("entities", {}):
            hass.data["alexa"]["entities"].pop(DOMAIN)
        
        # Unload services
        await async_unload_services(hass)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)