"""Constants for the Pioneer AVR LX83 integration."""
from datetime import timedelta

from homeassistant.components.media_player import MediaPlayerEntityFeature
from homeassistant.const import STATE_OFF, STATE_ON

DOMAIN = "pioneer_avr_lx83"
DEFAULT_NAME = "Pioneer AVR"
DEFAULT_PORT = 23
DEFAULT_TIMEOUT = 5

# Update intervals
SCAN_INTERVAL = timedelta(seconds=10)
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Configuration
CONF_SOURCES = "sources"

# Features
SUPPORT_PIONEER = (
    MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
)

# Default sources mapping
DEFAULT_SOURCES = {
    "CD": "10",
    "Tuner": "11",
    "Phono": "12",
    "DVD": "13",
    "TV/Sat": "14",
    "DVR/BDR": "15",
    "Video": "16",
    "iPod/USB": "17",
    "NET": "18",
}

# Commands
CMD_POWER_ON = "PO"
CMD_POWER_OFF = "PF"
CMD_POWER_QUERY = "?P"
CMD_VOLUME = "VL"
CMD_VOLUME_QUERY = "?V"
CMD_MUTE_ON = "MO"
CMD_MUTE_OFF = "MF"
CMD_MUTE_QUERY = "?M"
CMD_SOURCE = "FN"
CMD_SOURCE_QUERY = "?F"

