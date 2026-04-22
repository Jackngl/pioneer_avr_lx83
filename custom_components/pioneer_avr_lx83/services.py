"""Services for Pioneer AVR LX83."""
import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

# Use literal to avoid importing homeassistant.components.media_player at package load
# (config flow would then load the whole package and trigger a 500)
MEDIA_PLAYER_DOMAIN = "media_player"
from .voice_commands import get_intent_from_command

_LOGGER = logging.getLogger(__name__)

ATTR_COMMAND = "command"
ATTR_ENTITY_ID = "entity_id"

SERVICE_PROCESS_VOICE_COMMAND = "process_voice_command"
SERVICE_SEND_RAW_COMMAND = "send_raw_command"

PROCESS_VOICE_COMMAND_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
    vol.Required(ATTR_COMMAND): cv.string,
})

SEND_RAW_COMMAND_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
    vol.Required(ATTR_COMMAND): cv.string,
})

async def async_setup_services(hass: HomeAssistant):
    """Set up services for Pioneer AVR LX83."""
    
    async def async_process_voice_command(call: ServiceCall):
        """Process a voice command."""
        entity_id = call.data[ATTR_ENTITY_ID]
        command = call.data[ATTR_COMMAND]
        
        # Get the media player entity from our domain data
        entity = None
        for item in hass.data.get(DOMAIN, {}).values():
            # Check if the item is our PioneerAVR entity and matches the entity_id
            if hasattr(item, "entity_id") and item.entity_id == entity_id:
                entity = item
                break
                
        if not entity:
            _LOGGER.error("Entity %s not found in %s", entity_id, DOMAIN)
            return
            
        # Get the intent from the command
        intent = get_intent_from_command(command)
        if not intent:
            _LOGGER.warning("No intent found for command: %s", command)
            return
            
        # Execute the intent
        if intent == "turn_on":
            await entity.async_turn_on()
        elif intent == "turn_off":
            await entity.async_turn_off()
        elif intent == "volume_up":
            await entity.async_volume_up()
        elif intent == "volume_down":
            await entity.async_volume_down()
        elif intent == "mute":
            await entity.async_mute_volume(True)
        elif intent == "unmute":
            await entity.async_mute_volume(False)
        elif intent.startswith("select_source_"):
            source = intent.replace("select_source_", "")
            await entity.async_select_source(source)
        elif intent.startswith("select_sound_mode_"):
            mode = intent.replace("select_sound_mode_", "")
            await entity.async_select_sound_mode(mode)
        else:
            _LOGGER.warning("Unknown intent: %s", intent)
    
    async def async_send_raw_command(call: ServiceCall):
        """Send a raw command to the AVR."""
        entity_id = call.data[ATTR_ENTITY_ID]
        command = call.data[ATTR_COMMAND]
        
        entity = None
        for item in hass.data.get(DOMAIN, {}).values():
            if hasattr(item, "entity_id") and item.entity_id == entity_id:
                entity = item
                break
                
        if entity:
            await entity.async_send_raw_command(command)
        else:
            _LOGGER.error("Entity %s not found for raw command", entity_id)

    # Register the services
    hass.services.async_register(
        DOMAIN,
        SERVICE_PROCESS_VOICE_COMMAND,
        async_process_voice_command,
        schema=PROCESS_VOICE_COMMAND_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_RAW_COMMAND,
        async_send_raw_command,
        schema=SEND_RAW_COMMAND_SCHEMA,
    )
    
    return True

async def async_unload_services(hass: HomeAssistant):
    """Unload Pioneer AVR LX83 services."""
    # Remove the registered service
    if hass.services.has_service(DOMAIN, SERVICE_PROCESS_VOICE_COMMAND):
        hass.services.async_remove(DOMAIN, SERVICE_PROCESS_VOICE_COMMAND)
    
    return True