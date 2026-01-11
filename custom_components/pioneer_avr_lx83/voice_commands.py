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
    ],
    "select_source_bluray": [
        "passe sur le bluray",
        "mets le lecteur bluray",
        "switch to bluray",
    ],
    "select_sound_mode_movie": [
        "mode cinéma",
        "passe en mode film",
        "movie mode",
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