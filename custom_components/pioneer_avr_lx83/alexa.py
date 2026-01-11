"""Alexa integration for Pioneer AVR LX83."""
from homeassistant.components.alexa.entities import AlexaEntity
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.const import (
    STATE_OFF,
    STATE_ON,
    STATE_PAUSED,
    STATE_PLAYING,
)
from homeassistant.components.alexa.const import (
    CONF_DISPLAY_CATEGORIES,
    DISPLAY_CATEGORY_SPEAKER,
)

class PioneerAVRAlexaEntity(AlexaEntity):
    """Representation of a Pioneer AVR as an Alexa entity."""

    def __init__(self, media_player):
        """Initialize the Alexa entity."""
        self.media_player = media_player
        self._name = media_player.name

    def friendly_name(self):
        """Return the friendly name of the device."""
        return self._name

    def display_categories(self):
        """Return the display categories for this entity."""
        return [DISPLAY_CATEGORY_SPEAKER]

    def is_on(self):
        """Return true if the device is on."""
        return self.media_player.state != STATE_OFF

    async def async_turn_on(self, **kwargs):
        """Turn the device on."""
        await self.media_player.async_turn_on()

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        await self.media_player.async_turn_off()

    async def async_set_volume(self, volume):
        """Set volume level."""
        await self.media_player.async_set_volume_level(volume / 100.0)

    async def async_mute(self):
        """Mute the volume."""
        await self.media_player.async_mute_volume(True)

    async def async_unmute(self):
        """Unmute the volume."""
        await self.media_player.async_mute_volume(False)

    async def async_play(self):
        """Send play command."""
        await self.media_player.async_media_play()

    async def async_pause(self):
        """Send pause command."""
        await self.media_player.async_media_pause()

    async def async_select_source(self, source):
        """Select input source."""
        await self.media_player.async_select_source(source)