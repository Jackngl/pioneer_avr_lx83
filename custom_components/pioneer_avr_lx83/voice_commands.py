"""Voice command definitions for Pioneer AVR LX83."""

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
    "select_source_tv": [
        "passe sur la télé",
        "mets la télévision",
        "switch to tv",
        " sur tv",
        " sur la tv",
        " à la tv",
        " sur la télé",
    ],
    "select_source_hdmi1": [
        "hdmi 1",
        "hdmi un",
        "hdmi1",
    ],
    "select_source_hdmi2": [
        "hdmi 2",
        "hdmi deux",
        "hdmi2",
    ],
    "select_source_hdmi3": [
        "hdmi 3",
        "hdmi trois",
        "hdmi3",
    ],
    "select_source_hdmi4": [
        "hdmi 4",
        "hdmi quatre",
        "hdmi4",
    ],
    "select_source_hdmi5": [
        "hdmi 5",
        "hdmi cinq",
        "hdmi5",
    ],
    "select_source_bluray": [
        "passe sur le bluray",
        "mets le lecteur bluray",
        "switch to bluray",
        "bluray",
        "blu-ray",
    ],
    "select_source_bluetooth": [
        "bluetooth",
        "dent bleue",
    ],
    "select_sound_mode_movie": [
        "mode cinéma",
        "passe en mode film",
        "movie mode",
        "mode film",
    ],
    "select_sound_mode_music": [
        "mode musique",
        "passe en mode musique",
        "music mode",
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