"""Tests for Pioneer AVR LX83 media player."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.pioneer_avr_lx83.const import DOMAIN
from custom_components.pioneer_avr_lx83.media_player import PioneerAVR


@pytest.fixture
def mock_hass():
    """Mock Home Assistant."""
    hass = MagicMock()
    hass.async_add_executor_job = AsyncMock()
    return hass


@pytest.fixture
def pioneer_avr(mock_hass):
    """Create a Pioneer AVR instance."""
    return PioneerAVR(mock_hass, "Test AVR", "192.168.1.100", 23)


def test_pioneer_avr_init(pioneer_avr):
    """Test Pioneer AVR initialization."""
    assert pioneer_avr._name == "Test AVR"
    assert pioneer_avr._host == "192.168.1.100"
    assert pioneer_avr._port == 23


def test_pioneer_avr_name(pioneer_avr):
    """Test Pioneer AVR name property."""
    assert pioneer_avr.name == "Test AVR"


def test_pioneer_avr_source_list(pioneer_avr):
    """Test Pioneer AVR source list."""
    sources = pioneer_avr.source_list
    assert isinstance(sources, list)
    assert len(sources) > 0

