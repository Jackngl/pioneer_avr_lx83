"""Voice command definitions for Pioneer AVR LX83.

This module is used by the process_voice_command service for custom voice integrations
(not for Alexa Smart Home, which uses Home Assistant's native Alexa integration).
"""

VOICE_COMMANDS = {
    "turn_on": [
        "allume l'amplificateur",
        "allume le pioneer",
        "mets en marche l'amplificateur",
        "turn on the amplifier",
        "turn on the pioneer",
    ],
    "turn_off": [
        "éteins l'amplificateur",
        "éteins le pioneer",
        "arrête l'amplificateur",
        "turn off the amplifier",
        "turn off the pioneer",
    ],
    "volume_up": [
        "augmente le volume",
        "monte le son",
        "plus fort",
        "increase volume",
        "volume up",
    ],
    "volume_down": [
        "baisse le volume",
        "diminue le son",
        "moins fort",
        "decrease volume",
        "volume down",
    ],
    "mute": [
        "coupe le son",
        "mute",
        "silence",
    ],
    "unmute": [
        "remets le son",
        "unmute",
        "restore sound",
    ],
    # Sources (use Pioneer source names as they appear in Home Assistant)
    "select_source_TV": [
        "passe sur la télé",
        "mets la télévision",
        "switch to tv",
        "télé",
        "tv",
        "télévision",
    ],
    "select_source_Satellite": [
        "passe sur satellite",
        "switch to satellite",
    ],
    "select_source_DVD": [
        "passe sur dvd",
        "switch to dvd",
    ],
    "select_source_CD": [
        "passe sur cd",
        "switch to cd",
    ],
    "select_source_Tuner": [
        "passe sur le tuner",
        "passe sur la radio",
        "switch to tuner",
        "switch to radio",
    ],
    "select_source_Blu-ray": [
        "passe sur le bluray",
        "mets le lecteur bluray",
        "switch to bluray",
    ],
    "select_source_HDMI 1": [
        "passe sur hdmi 1",
        "switch to hdmi 1",
        "hdmi 1",
        "hdmi one",
        "hdmi un",
    ],
    "select_source_HDMI 2": [
        "passe sur hdmi 2",
        "switch to hdmi 2",
    ],
    "select_source_HDMI 3": [
        "passe sur hdmi 3",
        "switch to hdmi 3",
    ],
    "select_source_HDMI 4": [
        "passe sur hdmi 4",
        "switch to hdmi 4",
    ],
    "select_source_HDMI 5": [
        "passe sur hdmi 5",
        "switch to hdmi 5",
    ],
    "select_source_iPod": [
        "passe sur ipod",
        "switch to ipod",
    ],
    "select_source_Bluetooth": [
        "passe sur bluetooth",
        "switch to bluetooth",
        "bluetooth",
    ],
    "select_source_Phono": [
        "passe sur phono",
        "switch to phono",
    ],
    # Sound modes (use Pioneer mode names as they appear in Home Assistant)
    "select_sound_mode_Stereo": [
        "mode stéréo",
        "passe en stéréo",
        "stereo mode",
        "switch to stereo",
    ],
    "select_sound_mode_Direct": [
        "mode direct",
        "passe en direct",
        "direct mode",
    ],
    "select_sound_mode_Pure Direct": [
        "mode pure direct",
        "passe en pure direct",
        "pure direct mode",
    ],
    "select_sound_mode_Auto Surround": [
        "mode auto surround",
        "passe en auto surround",
        "auto surround mode",
    ],
    "select_sound_mode_THX Cinema": [
        "mode cinéma",
        "passe en mode film",
        "mode thx",
        "movie mode",
        "cinema mode",
        "thx cinema",
    ],
    "select_sound_mode_THX Music": [
        "mode musique",
        "passe en mode musique",
        "music mode",
        "thx music",
    ],
    "select_sound_mode_Advanced Game": [
        "mode jeu",
        "passe en mode jeu",
        "game mode",
    ],
}

def get_intent_from_command(command):
    """Get the intent from a voice command."""
    command = command.lower()
    
    for intent, phrases in VOICE_COMMANDS.items():
        for phrase in phrases:
            if phrase in command:
                return intent
                
    return None