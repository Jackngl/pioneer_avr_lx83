def __init__(
    self,
    hass: HomeAssistant,
    name: str,
    host: str,
    port: int,
) -> None:
    """Initialize the Pioneer AVR device."""
    self.hass = hass
    # Modifions l'identifiant unique pour éviter les conflits avec DLNA
    self._attr_unique_id = f"pioneer_telnet_{host}_{port}"
    self._attr_device_info = {
        "identifiers": {(DOMAIN, self._attr_unique_id)},
        "name": name,
        "manufacturer": "Pioneer",
        "model": "AVR LX83",
    }
    self._host = host
    self._port = port
    self._name = name
    self._state = STATE_OFF
    self._volume = 0.0
    self._is_muted = False
    self._source = None
    self._sources = DEFAULT_SOURCES
    self._available = True