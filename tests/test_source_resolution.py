"""Test source resolution logic."""
import pytest
from unittest.mock import MagicMock
from custom_components.pioneer_avr_lx83.media_player import PioneerAVR

@pytest.fixture
def pioneer_avr():
    hass = MagicMock()
    return PioneerAVR(hass, "Test AVR", "localhost", 23)

def test_resolve_source_code(pioneer_avr):
    """Test source resolution for various inputs."""
    test_cases = [
        ("TV", ("05", "TV/Sat")),
        ("TV/Sat", ("05", "TV/Sat")),
        ("tv", ("05", "TV/Sat")),
        ("tv/sat", ("05", "TV/Sat")),
        ("Sat", ("05", "TV/Sat")),
        ("Television", None), # Expected failure currently
        ("Téle", None),       # Expected failure currently
        ("Tele", None),       # Expected failure currently
    ]

    for input_source, expected in test_cases:
        result = pioneer_avr._resolve_source_code(input_source)
        print(f"Input: '{input_source}' -> Result: {result}")
        if expected is None:
            assert result is None, f"Expected None for '{input_source}', got {result}"
        else:
            assert result == expected, f"Expected {expected} for '{input_source}', got {result}"

if __name__ == "__main__":
    # Manually run if executed as script
    p = pioneer_avr()
    test_resolve_source_code(p)
