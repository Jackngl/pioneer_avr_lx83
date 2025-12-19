"""Constants for the Pioneer AVR LX83 integration."""

from datetime import timedelta

from homeassistant.components.media_player import MediaPlayerEntityFeature
from homeassistant.const import STATE_OFF, STATE_ON

DOMAIN = "pioneer_avr_lx83"
DEFAULT_NAME = "Pioneer AVR"
DEFAULT_PORT = 23
DEFAULT_TIMEOUT = 10  # seconds instead of 5
# Update intervals
SCAN_INTERVAL = timedelta(seconds=10)
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
COMMAND_TERMINATOR = "\r"
COMMAND_PAUSE = 0.3  # seconds between sequential telnet commands
VOLUME_MAX = 185  # Pioneer absolute volume steps
VOLUME_DB_OFFSET = 85  # Step offset when AVR front panel shows dB

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
    | MediaPlayerEntityFeature.PLAY
    | MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.SELECT_SOUND_MODE
)

MAX_SOURCE_SLOTS = 60

# Default sources mapping - friendly labels shown in HA
DEFAULT_SOURCES = {
    "Phono": "00",
    "CD": "01",
    "Tuner": "02",
    "CDR/Tape": "03",
    "DVD": "04",
    "TV/Sat": "05",
    "Video 1": "10",
    "Multi Ch In": "12",
    "Video 2": "14",
    "DVR/BDR": "15",
    "iPod/USB": "17",
    "XM Radio": "18",
    "HDMI 1": "19",
    "HDMI 2": "20",
    "HDMI 3": "21",
    "HDMI 4": "22",
    "HDMI 5": "23",
    "Blu-ray": "25",
    "Home Media Gallery": "26",
    "HDMI Cycle": "31",
    "Bluetooth": "33",
}

# Case-insensitive aliases to improve dashboard usability
SOURCE_ALIASES = {
    "phono": "00",
    "cd": "01",
    "tuner": "02",
    "cdr/tape": "03",
    "tape": "03",
    "dvd": "04",
    "tv": "05",
    "tv/sat": "05",
    "sat": "05",
    "video1": "10",
    "video 1": "10",
    "multi ch": "12",
    "multich": "12",
    "video2": "14",
    "video 2": "14",
    "dvr": "15",
    "bdr": "15",
    "ipod": "17",
    "usb": "17",
    "xm": "18",
    "xm radio": "18",
    "hdmi": "19",
    "hdmi1": "19",
    "hdmi2": "20",
    "hdmi3": "21",
    "hdmi4": "22",
    "hdmi5": "23",
    "bd": "25",
    "blu-ray": "25",
    "bluray": "25",
    "bd/dvd": "25",
    "hmg": "26",
    "net": "26",
    "network": "26",
    "hdmi cycl": "31",
    "hdmi cycle": "31",
    "adapter port": "33",
    "adapter": "33",
    "bluetooth": "33",
}

# Listening modes (adapted from Pioneer IP documentation and aiopioneer project)
# Note: Some Pioneer models return extended codes (e.g., "0401" for Auto Surround)
# We map both the standard codes and extended codes to the same mode names
DEFAULT_LISTENING_MODES = {
    "Auto Surround": "0006",
    "Direct": "0007",
    "Pure Direct": "0008",
    "Stereo": "0001",
    "Standard": "0010",
    "Extended Stereo": "0112",
    "Advanced Game": "0118",
    "THX Cinema": "0056",
    "THX Music": "0069",
    "Optimum Surround": "0152",
    "Eco Mode": "0200",
}

# Mapping des codes étendus retournés par certains modèles Pioneer
# Format: code_etendu -> code_standard
LISTENING_MODE_CODE_MAPPING = {
    "0401": "0006",  # Auto Surround (code étendu)
    "040d": "0006",  # Auto Surround (variante)
    "0501": "0001",  # Stereo (code étendu)
    "0601": "0007",  # Direct (code étendu)
    "0701": "0008",  # Pure Direct (code étendu)
}

LISTENING_MODE_ALIASES = {
    "auto": "0006",
    "auto surround": "0006",
    "direct": "0007",
    "pure": "0008",
    "pure direct": "0008",
    "stereo": "0001",
    "standard": "0010",
    "extended": "0112",
    "extended stereo": "0112",
    "game": "0118",
    "advanced game": "0118",
    "thx": "0056",
    "thx cinema": "0056",
    "thx music": "0069",
    "optimum": "0152",
    "optimum surround": "0152",
    "eco": "0200",
    "eco mode": "0200",
}

# Commands
CMD_POWER_ON = "PO"
CMD_POWER_OFF = "PF"
CMD_POWER_QUERY = "?P"
CMD_VOLUME = "VL"
CMD_VOLUME_QUERY = "?V"
CMD_VOLUME_UP = "VU"
CMD_VOLUME_DOWN = "VD"
CMD_MUTE_ON = "MO"
CMD_MUTE_OFF = "MF"
CMD_MUTE_QUERY = "?M"
CMD_SOURCE = "FN"
CMD_SOURCE_QUERY = "?F"
CMD_SOURCE_UP = "FU"
CMD_SOURCE_DOWN = "FD"
CMD_SOURCE_NAME_QUERY = "?RGB"

# Commandes supplémentaires pour les fonctionnalités avancées
# Mode d'écoute
CMD_LISTENING_MODE = "SR"
CMD_LISTENING_MODE_QUERY = "?L"

# Media transport
CMD_MEDIA_PLAY = "10NW"
CMD_MEDIA_PAUSE = "11NW"

# Contrôle de tonalité
CMD_TONE_ON = "TO1"
CMD_TONE_BYPASS = "TO0"
CMD_TONE_QUERY = "?TO"

# Contrôle des basses
CMD_BASS_UP = "BI"
CMD_BASS_DOWN = "BD"
CMD_BASS_QUERY = "?BA"

# Contrôle des aigus
CMD_TREBLE_UP = "TI"
CMD_TREBLE_DOWN = "TD"
CMD_TREBLE_QUERY = "?TR"

# Configuration des haut-parleurs
CMD_SPEAKERS = "SPK"
CMD_SPEAKERS_OFF = "0SPK"
CMD_SPEAKERS_A = "1SPK"
CMD_SPEAKERS_B = "2SPK"
CMD_SPEAKERS_A_B = "3SPK"

# Configuration des sorties HDMI
CMD_HDMI_OUTPUT = "HO"
CMD_HDMI_OUT_ALL = "0HO"
CMD_HDMI_OUT_1 = "1HO"
CMD_HDMI_OUT_2 = "2HO"

# Configuration audio HDMI
CMD_HDMI_AUDIO_AMP = "0HA"
CMD_HDMI_AUDIO_THROUGH = "1HA"

# Réglage PQLS
CMD_PQLS_OFF = "0PQ"
CMD_PQLS_AUTO = "1PQ"

# Commandes Zone 2
CMD_ZONE2_POWER_ON = "APO"
CMD_ZONE2_POWER_OFF = "APF"
CMD_ZONE2_POWER_QUERY = "?AP"
CMD_ZONE2_INPUT = "ZS"
CMD_ZONE2_INPUT_QUERY = "?ZS"
CMD_ZONE2_VOLUME_UP = "ZU"
CMD_ZONE2_VOLUME_DOWN = "ZD"
CMD_ZONE2_VOLUME = "ZV"
CMD_ZONE2_VOLUME_QUERY = "?ZV"
CMD_ZONE2_MUTE = "Z2MO"
CMD_ZONE2_UNMUTE = "Z2MF"
CMD_ZONE2_MUTE_QUERY = "?Z2M"

# Commandes Zone 3
CMD_ZONE3_POWER_ON = "BPO"
CMD_ZONE3_POWER_OFF = "BPF"
CMD_ZONE3_POWER_QUERY = "?BP"
CMD_ZONE3_INPUT = "ZT"
CMD_ZONE3_INPUT_QUERY = "?ZT"
CMD_ZONE3_VOLUME_UP = "YU"
CMD_ZONE3_VOLUME_DOWN = "YD"
CMD_ZONE3_VOLUME = "YV"
CMD_ZONE3_VOLUME_QUERY = "?YV"
CMD_ZONE3_MUTE = "Z3MO"
CMD_ZONE3_UNMUTE = "Z3MF"
CMD_ZONE3_MUTE_QUERY = "?Z3M"

# Commandes du tuner radio
CMD_TUNER_FREQ_UP = "TFI"
CMD_TUNER_FREQ_DOWN = "TFD"
CMD_TUNER_FREQ_QUERY = "?FR"
CMD_TUNER_BAND = "TB"
CMD_TUNER_PRESET = "TP"
CMD_TUNER_CLASS = "TC"
CMD_TUNER_PRESET_UP = "TPI"
CMD_TUNER_PRESET_DOWN = "TPD"
CMD_TUNER_PRESET_QUERY = "?TP"

# Affichage
CMD_DISPLAY_INFO_QUERY = "?FL"
