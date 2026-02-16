"""Constants for the Pioneer AVR LX83 integration."""

from datetime import timedelta

from homeassistant.components.media_player import MediaPlayerEntityFeature
from homeassistant.const import STATE_OFF, STATE_ON

DOMAIN = "pioneer_avr_lx83"
DEFAULT_NAME = "Pioneer"
DEFAULT_PORT = 23
DEFAULT_TIMEOUT = 10  # seconds instead of 5
UPDATE_TIMEOUT = 2  # seconds - shorter timeout for update queries to avoid exceeding scan interval
# Update intervals
SCAN_INTERVAL = timedelta(seconds=10)
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
COMMAND_TERMINATOR = "\r"
# IMPORTANT: Délai entre chaque commande Telnet (100ms recommandé par Pioneer)
# Ce délai évite de saturer le processeur réseau de l'amplificateur
COMMAND_PAUSE = 0.1  # 100ms entre les commandes séquentielles
VOLUME_MAX = 185  # Pioneer absolute volume steps
VOLUME_DB_OFFSET = 85  # Step offset when AVR front panel shows dB

# Configuration
CONF_SOURCES = "sources"
CONF_SOUND_MODES = "sound_modes"

# Attributes
ATTR_COMMAND = "command"
ATTR_SOURCE_CODE = "source_code"
ATTR_SOUND_MODE_CODE = "sound_mode_code"

# Services
SERVICE_SEND_COMMAND = "send_command"
SERVICE_PROCESS_VOICE_COMMAND = "process_voice_command"

# Alexa
ALEXA_INTERFACE = "Alexa"
ALEXA_CAPABILITY_INTERFACE = "Alexa.PowerController"
ALEXA_CAPABILITY_INTERFACE_VOLUME = "Alexa.Speaker"
ALEXA_CAPABILITY_INTERFACE_PLAYBACK = "Alexa.PlaybackController"
ALEXA_CAPABILITY_INTERFACE_INPUT = "Alexa.InputController"

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
    "Multi Ch": "12",
    "Video 2": "14",
    "DVR/BDR": "15",
    "iPod/USB": "17",
    "XM Radio": "18",
    "HDMI 1": "19",
    "HDMI 2": "20",
    "HDMI 3": "21",
    "HDMI 4": "22",
    "HDMI 5": "23",
    "BD": "25",
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
    "télé": "05",
    "télévision": "05",
    "television": "05",
    "video1": "10",
    "video 1": "10",
    "multi ch": "12",
    "multich": "12",
    "multi ch in": "12",
    "video2": "14",
    "video 2": "14",
    "dvr": "15",
    "bdr": "15",
    "ipod": "17",
    "usb": "17",
    "ipod/usb": "17",
    "xm": "18",
    "xm radio": "18",
    "hdmi": "19",
    "hdmi1": "19",
    "hdmi 1": "19",
    "hdmi un": "19",
    "hdmi2": "20",
    "hdmi 2": "20",
    "hdmi deux": "20",
    "hdmi3": "21",
    "hdmi 3": "21",
    "hdmi trois": "21",
    "hdmi4": "22",
    "hdmi 4": "22",
    "hdmi quatre": "22",
    "hdmi5": "23",
    "hdmi 5": "23",
    "hdmi cinq": "23",
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
    "bt": "33",
}

# Listening modes (adapted from Pioneer IP documentation and aiopioneer project)
# Note: Some Pioneer models return extended codes (e.g., "0401" for Auto Surround)
# We map both the standard codes and extended codes to the same mode names
# IMPORTANT: THX modes use codes starting with 01xx, not 00xx
DEFAULT_LISTENING_MODES = {
    # Cycle Stéréo (SR0001) - Vérifié LX83
    "Stereo": "0001",
    "ALC": "0153",  # Auto Level Control (LM=0002)
    "F.S.S.A. Advance": "0154",  # Front Stage Surround Advance (LM=0003)
    "F.S. Surround": "0155",  # Front Stage Surround (LM=0004)
    # Auto / Direct
    "Auto Surround": "0006",
    "Direct": "0007",
    "Pure Direct": "0008",
    # Dolby / DTS (cycle SR0010 + commandes directes)
    "Standard": "0010",
    "Neo:6 Cinema": "0011",
    "Neo:6 Music": "0012",
    "PRO LOGIC II Movie": "0013",
    "PRO LOGIC II Music": "0014",
    "PRO LOGIC II Game": "0015",
    "Dolby Pro Logic": "0016",  # LM=0107, cycle uniquement
    "Neural Surround": "0017",  # LM=010b, cycle uniquement
    "Dolby Surround": "0151",
    # THX Direct (SR0051-0053)
    "THX Cinema": "0051",
    "THX Music": "0052",
    "THX Games": "0053",
    "THX Select2 Cinema": "0054",
    "THX Select2 Music": "0055",
    "THX Select2 Games": "0056",
    "THX Surround EX": "0057",
    # THX Combinés (cycle SR0050 après Dolby, display only)
    "PL II Music + THX": "0058",
    "Neo:6 Music + THX": "0059",
    "PL II Game + THX": "0060",
    # DSP / Advanced Surround (cycle SR0100 + commandes directes)
    "Action": "0101",
    "Sci-Fi": "0102",
    "Drama": "0103",
    "Entertainment Show": "0104",
    "Mono Film": "0105",
    "Expanded Theater": "0106",
    "Classical": "0107",
    "Rock/Pop": "0108",
    "Unplugged": "0109",
    "TV Surround": "0110",  # LM=0207, cycle uniquement
    "Phones Surround": "0111",
    "Extended Stereo": "0112",
    "Sports": "0113",  # LM=0209, cycle uniquement
    "Advanced Game": "0118",
    # Autres
    "Optimum Surround": "0152",
}

# Mapping des codes LM retournés par le LX83 vers les codes standards
# Format: code_LM_reponse -> code_standard (clé dans DEFAULT_LISTENING_MODES)
# VÉRIFIÉ PAR TESTS TELNET DIRECTS (2026-02-14)
LISTENING_MODE_CODE_MAPPING = {
    # === Cycle Stéréo (SR0001) ===
    "0001": "0001",  # Stereo
    "0002": "0153",  # ALC
    "0003": "0154",  # F.S.S.A. Advance
    "0004": "0155",  # F.S. Surround
    
    # === Auto / Direct ===
    "040e": "0006",  # Auto Surround
    "0401": "0006",  # Auto Surround (variant)
    "0601": "0007",  # Direct
    "0701": "0008",  # Pure Direct
    "0501": "0151",  # Dolby Surround
    "0881": "0152",  # Optimum Surround
    
    # === Cycle Dolby/DTS (SR0010) - réponses LM 01xx ===
    "0102": "0013",  # PRO LOGIC II Movie
    "0104": "0014",  # PRO LOGIC II Music
    "0106": "0015",  # PRO LOGIC II Game
    "0107": "0016",  # Dolby Pro Logic
    "0108": "0011",  # Neo:6 Cinema
    "0109": "0012",  # Neo:6 Music
    "010b": "0017",  # Neural Surround
    
    # === THX Direct (SR0051-0053) ===
    "0303": "0051",  # THX Cinema
    "0302": "0052",  # THX Music
    "0304": "0053",  # THX Games
    
    # === THX Combinés (cycle SR0050 après Dolby) ===
    "0307": "0058",  # PL II Music + THX
    "0309": "0059",  # Neo:6 Music + THX
    "030c": "0060",  # PL II Game + THX
    "030a": "0057",  # THX Surround EX
    
    # === DSP / Advanced Surround - réponses LM 02xx ===
    "0201": "0101",  # Action
    "0202": "0103",  # Drama
    "0203": "0102",  # Sci-Fi
    "0204": "0105",  # Mono Film
    "0205": "0104",  # Entertainment Show
    "0206": "0106",  # Expanded Theater
    "0207": "0110",  # TV Surround
    "0208": "0118",  # Advanced Game
    "0209": "0113",  # Sports
    "020a": "0107",  # Classical
    "020b": "0108",  # Rock/Pop
    "020c": "0109",  # Unplugged
    "020d": "0112",  # Extended Stereo
}

LISTENING_MODE_ALIASES = {
    # Stéréo
    "stereo": "0001",
    "stéréo": "0001",
    "alc": "0153",
    # Auto / Direct
    "auto": "0006",
    "auto surround": "0006",
    "stream direct": "0006",
    "direct": "0007",
    "pure": "0008",
    "pure direct": "0008",
    # Dolby / DTS
    "standard": "0010",
    "dolby": "0013",
    "dolby cinema": "0013",
    "dolby cinéma": "0013",
    "dolby musique": "0014",
    "dolby music": "0014",
    "pro logic": "0013",
    "pro logic ii": "0013",
    "pro logic ii movie": "0013",
    "pro logic ii music": "0014",
    "pro logic ii game": "0015",
    "neo6 cinema": "0011",
    "neo:6 cinema": "0011",
    "neo6 music": "0012",
    "neo:6 music": "0012",
    "neural": "0017",
    "neural surround": "0017",
    "dolby surround": "0151",
    # THX
    "thx": "0051",
    "thx cinema": "0051",
    "thx cinéma": "0051",
    "thx music": "0052",
    "thx musique": "0052",
    "thx games": "0053",
    "thx jeux": "0053",
    "thx select2 cinema": "0054",
    "thx select2 music": "0055",
    "thx select2 games": "0056",
    "thx surround ex": "0057",
    # DSP
    "extended": "0112",
    "extended stereo": "0112",
    "game": "0118",
    "jeu": "0118",
    "advanced game": "0118",
    "action": "0101",
    "drama": "0103",
    "sci-fi": "0102",
    "classical": "0107",
    "classique": "0107",
    "rock": "0108",
    "rock/pop": "0108",
    "sports": "0113",
    "sport": "0113",
    # Autres
    "optimum": "0152",
    "optimum surround": "0152",
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