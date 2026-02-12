"""Standalone reproduction of source resolution logic."""

# Copied from const.py
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
    "television": "05",
    "télévision": "05",
    "télé": "05",
    "tele": "05",
    "tv sat": "05",
    "tv-sat": "05",
    "sat tv": "05",
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

class PioneerAVR:
    def __init__(self):
        self._sources = dict(DEFAULT_SOURCES)
        self._source_code_to_name = {}
        for name, code in self._sources.items():
            if code not in self._source_code_to_name:
                self._source_code_to_name[code] = name
        
        # Add Alexa-compatible aliases to sources for discovery
        alexa_aliases = {
            "TV": "05",
            "Satellite": "05",
            "Télé": "05",
            "Télévision": "05",
            "Aux 1": "03",
            "Game": "12",
            "Input 1": "15",
            "iPod": "17",
            "HD Radio": "18",
            "Media Player": "26",
            "Bluetooth": "33",
            "HDMI 1": "19",
            "HDMI un": "19",
            "HDMI one": "19",
        }
        for alias_name, code in alexa_aliases.items():
            if alias_name not in self._sources:
                self._sources[alias_name] = code
        
        self._source_aliases = {
            name.lower(): code for name, code in self._sources.items()
        }
        self._source_aliases.update(SOURCE_ALIASES)

    def _resolve_source_code(self, label):
        """Return (code, canonical_name) for a source label, case-insensitively."""
        if not label:
            return None
        clean_label = label.strip()
        if not clean_label:
            return None
        if clean_label in self._sources:
            return self._sources[clean_label], clean_label
        lowered = clean_label.lower()
        alias_code = self._source_aliases.get(lowered)
        if alias_code:
            canonical = self._source_code_to_name.get(alias_code, clean_label)
            return alias_code, canonical
        return None

def test():
    avr = PioneerAVR()
    test_cases = [
        ("TV", ("05", "TV")),
        ("Télé", ("05", "Télé")),
        ("Télévision", ("05", "Télévision")),
        ("HDMI un", ("19", "HDMI un")),
        ("Bluetooth", ("33", "Bluetooth")),
        ("bluetooth", ("33", "Bluetooth")),
        ("BlueTooth", ("33", "Bluetooth")),
        ("HDMI 1", ("19", "HDMI 1")),
    ]

    for input_source, expected in test_cases:
        result = avr._resolve_source_code(input_source)
        print(f"Input: '{input_source}' -> Result: {result} - {'PASS' if result == expected else 'FAIL'}")

if __name__ == "__main__":
    test()
