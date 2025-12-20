"""Constants for the Pioneer AVR LX83 integration."""

from datetime import timedelta

DOMAIN = "pioneer_avr_lx83"

# Configuration
DEFAULT_PORT = 23
DEFAULT_TIMEOUT = 10  # seconds
SCAN_INTERVAL = timedelta(seconds=10)
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
COMMAND_PAUSE = 0.1  # 100ms between commands - CRITICAL to avoid overloading the network processor

# Volume
VOLUME_MAX = 185  # Pioneer max volume step
VOLUME_DB_OFFSET = 85  # Offset for dB conversion

# Sources
DEFAULT_SOURCES = {
    "CD": "01",
    "Tuner": "02",
    "CDR/TAPE": "03",
    "DVD": "04",
    "TV/Sat": "05",
    "VIDEO 1": "10",
    "MULTI CH IN": "12",
    "VIDEO 2": "14",
    "DVR/BDR": "15",
    "iPod/USB": "17",
    "XM RADIO": "18",
    "HDMI 1": "19",
    "HDMI 2": "20",
    "HDMI 3": "21",
    "HDMI 4": "22",
    "HDMI 5": "23",
    "BD": "25",
    "HMG": "26",
    "HDMI CYCLE": "31",
    "Bluetooth": "33",
    "Phono": "00",
}

# Source aliases (case insensitive)
SOURCE_ALIASES = {
    "cd": "01",
    "tuner": "02",
    "cdr": "03",
    "tape": "03",
    "dvd": "04",
    "tv": "05",
    "sat": "05",
    "video1": "10",
    "video 1": "10",
    "multi": "12",
    "multi ch": "12",
    "video2": "14",
    "video 2": "14",
    "dvr": "15",
    "bdr": "15",
    "ipod": "17",
    "usb": "17",
    "xm": "18",
    "hdmi1": "19",
    "hdmi 1": "19",
    "hdmi2": "20",
    "hdmi 2": "20",
    "hdmi3": "21",
    "hdmi 3": "21",
    "hdmi4": "22",
    "hdmi 4": "22",
    "hdmi5": "23",
    "hdmi 5": "23",
    "bd": "25",
    "bluray": "25",
    "blu-ray": "25",
    "hmg": "26",
    "home media gallery": "26",
    "hdmi cycle": "31",
    "hdmi cycl": "31",
    "bluetooth": "33",
    "bt": "33",
    "adapter": "33",
    "adapter port": "33",
    "phono": "00",
}

# Maximum source slots to query
MAX_SOURCE_SLOTS = 60

# Listening modes
DEFAULT_LISTENING_MODES = {
    # Modes standards
    "Stereo": "0001",
    "Auto Surround": "0006",
    "Direct": "0007",
    "Pure Direct": "0008",
    "Standard": "0010",
    "Extended Stereo": "0112",
    "Advanced Game": "0118",
    "Optimum Surround": "0152",
    
    # Modes Dolby/DTS directs
    "Dolby PL II Movie": "0013",
    "Dolby PL II Music": "0014",
    "Dolby Surround": "0151",
    
    # Modes THX
    "THX Cinema": "0101",
    "THX Music": "0102",
    "THX Games": "0103",
    "THX Select2 Cinema": "0105",
    "THX Select2 Music": "0106",
    "THX Select2 Games": "0107",
    "THX Surround EX": "0115",
}

# Listening mode aliases (case insensitive)
LISTENING_MODE_ALIASES = {
    "stereo": "0001",
    "auto": "0006",
    "auto surround": "0006",
    "direct": "0007",
    "pure": "0008",
    "pure direct": "0008",
    "standard": "0010",
    "ext.stereo": "0112",
    "extended stereo": "0112",
    "game": "0118",
    "advanced game": "0118",
    "optimum": "0152",
    "optimum surround": "0152",
    "dolby movie": "0013",
    "pl2 movie": "0013",
    "dolby music": "0014",
    "pl2 music": "0014",
    "dolby surround": "0151",
    "thx cinema": "0101",
    "thx music": "0102",
    "thx games": "0103",
    "thx select2 cinema": "0105",
    "thx ultra2 cinema": "0105",
    "thx select2 music": "0106",
    "thx ultra2 music": "0106",
    "thx select2 games": "0107",
    "thx ultra2 games": "0107",
    "thx surround ex": "0115",
}

# Nouveau dictionnaire pour les réponses de mode d'écoute
LISTENING_MODE_RESPONSES = {
    "0001": "Stereo",
    "0006": "Auto Surround",
    "0007": "Direct",
    "0008": "Pure Direct",
    "0102": "Dolby PL II Movie",
    "0104": "Dolby PL II Music",
    "0106": "Dolby PL II Game",
    "0107": "Dolby Pro Logic",
    "0108": "Neo:6 Cinema",
    "0109": "Neo:6 Music",
    "010b": "Neural Surround",
    "0101": "THX Cinema",
    "0102": "THX Music",
    "0103": "THX Games",
    "0105": "THX Select2 Cinema",
    "0106": "THX Select2 Music",
    "0107": "THX Select2 Games",
    "0115": "THX Surround EX",
    "020a": "Classical",
    "020b": "Rock/Pop",
    "020c": "Unplugged",
    "020d": "Extended Stereo",
    "0201": "Action",
    "0202": "Drama",
    "0203": "Sci-Fi",
    "0204": "Mono",
    "0205": "Entertainment Show",
    "0206": "Expanded",
    "0207": "TV Surround",
    "0208": "Advanced Game",
    "0209": "Sports",
    "0302": "Dolby PL II Movie + THX",
    "0303": "Dolby PL + THX Cinema",
    "0304": "Neo:6 Cinema + THX",
    "0307": "Dolby PL II Music + THX",
    "0309": "Neo:6 Music + THX",
    "030c": "Dolby PL II Game + THX",
    "0151": "Dolby Surround",
}

# Dictionnaire des cycles de modes audio
LISTENING_MODE_CYCLES = {
    # Cycle SR0010 (Modes Dolby/DTS standards)
    "0010": [
        {"code": "0102", "name": "DOLBY PLII MOVIE"},
        {"code": "0104", "name": "DOLBY PLII MUSIC"},
        {"code": "0106", "name": "DOLBY PLII GAME"},
        {"code": "0107", "name": "DOLBY PRO LOGIC"},
        {"code": "0108", "name": "Neo:6 CINEMA"},
        {"code": "0109", "name": "Neo:6 MUSIC"},
        {"code": "010b", "name": "NEURAL SURROUND"},
    ],
    
    # Cycle SR0050 (Modes Dolby/DTS + THX)
    "0050": [
        {"code": "030c", "name": "DOLBY PLII GAME + THX"},
        {"code": "0302", "name": "DOLBY PLII MOVIE + THX"},
        {"code": "0303", "name": "DOLBY PL + THX CINEMA"},
        {"code": "0304", "name": "Neo:6 CINEMA + THX"},
        {"code": "0307", "name": "DOLBY PLII MUSIC + THX"},
        {"code": "0309", "name": "Neo:6 MUSIC + THX"},
    ],
    
    # Cycle SR0100 (Modes DSP)
    "0100": [
        {"code": "020a", "name": "CLASSICAL"},
        {"code": "020b", "name": "ROCK/POP"},
        {"code": "020c", "name": "UNPLUGGED"},
        {"code": "020d", "name": "EXT.STEREO"},
        {"code": "0201", "name": "ACTION"},
        {"code": "0202", "name": "DRAMA"},
        {"code": "0203", "name": "SCI-FI"},
        {"code": "0204", "name": "MONO"},
        {"code": "0205", "name": "ENT.SHOW"},
        {"code": "0206", "name": "EXPANDED"},
        {"code": "0207", "name": "TV SURROUND"},
        {"code": "0208", "name": "ADVANCED GAME"},
        {"code": "0209", "name": "SPORTS"},
    ],
}

# Commands
CMD_POWER_ON = "PO"
CMD_POWER_OFF = "PF"
CMD_POWER_QUERY = "?P"

CMD_VOLUME_UP = "VU"
CMD_VOLUME_DOWN = "VD"
CMD_VOLUME = "VL"
CMD_VOLUME_QUERY = "?V"

CMD_MUTE_ON = "MO"
CMD_MUTE_OFF = "MF"
CMD_MUTE_QUERY = "?M"

CMD_SOURCE = "FN"
CMD_SOURCE_QUERY = "?F"
CMD_SOURCE_NAME_QUERY = "?RGB"

CMD_SOUND_MODE = "SR"
CMD_SOUND_MODE_QUERY = "?L"

CMD_PLAY = "10NW"
CMD_PAUSE = "11NW"

# Zone 2 commands
CMD_ZONE2_POWER_ON = "APO"
CMD_ZONE2_POWER_OFF = "APF"
CMD_ZONE2_POWER_QUERY = "?AP"
CMD_ZONE2_SOURCE = "ZS"
CMD_ZONE2_SOURCE_QUERY = "?ZS"
CMD_ZONE2_VOLUME_UP = "ZU"
CMD_ZONE2_VOLUME_DOWN = "ZD"
CMD_ZONE2_VOLUME = "ZV"
CMD_ZONE2_VOLUME_QUERY = "?ZV"
CMD_ZONE2_MUTE_ON = "Z2MO"
CMD_ZONE2_MUTE_OFF = "Z2MF"
CMD_ZONE2_MUTE_QUERY = "?Z2M"

# Zone 3 commands
CMD_ZONE3_POWER_ON = "BPO"
CMD_ZONE3_POWER_OFF = "BPF"
CMD_ZONE3_POWER_QUERY = "?BP"
CMD_ZONE3_SOURCE = "ZT"
CMD_ZONE3_SOURCE_QUERY = "?ZT"
CMD_ZONE3_VOLUME_UP = "YU"
CMD_ZONE3_VOLUME_DOWN = "YD"
CMD_ZONE3_VOLUME = "YV"
CMD_ZONE3_VOLUME_QUERY = "?YV"
CMD_ZONE3_MUTE_ON = "Z3MO"
CMD_ZONE3_MUTE_OFF = "Z3MF"
CMD_ZONE3_MUTE_QUERY = "?Z3M"

# Tuner commands
CMD_TUNER_FREQ_UP = "TFI"
CMD_TUNER_FREQ_DOWN = "TFD"
CMD_TUNER_FREQ_QUERY = "?FR"
CMD_TUNER_BAND = "TB"
CMD_TUNER_PRESET = "TP"
CMD_TUNER_CLASS = "TC"
CMD_TUNER_PRESET_UP = "TPI"
CMD_TUNER_PRESET_DOWN = "TPD"
CMD_TUNER_PRESET_QUERY = "?TP"

# Response prefixes
RESP_POWER = "PWR"
RESP_VOLUME = "VOL"
RESP_MUTE = "MUT"
RESP_SOURCE = "FN"
RESP_SOURCE_NAME = "RGB"
RESP_SOUND_MODE = "LM"