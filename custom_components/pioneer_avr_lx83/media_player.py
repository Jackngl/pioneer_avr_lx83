"""Support for Pioneer AVR LX83 receivers."""

from __future__ import annotations

import asyncio
import logging
import socket
import time

import voluptuous as vol

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    STATE_OFF,
    STATE_ON,
    STATE_PAUSED,
    STATE_PLAYING,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CMD_LISTENING_MODE,
    CMD_LISTENING_MODE_QUERY,
    CMD_MUTE_OFF,
    CMD_MUTE_ON,
    CMD_MUTE_QUERY,
    CMD_MEDIA_PAUSE,
    CMD_MEDIA_PLAY,
    CMD_POWER_OFF,
    CMD_POWER_ON,
    CMD_POWER_QUERY,
    CMD_SOURCE,
    CMD_SOURCE_NAME_QUERY,
    CMD_SOURCE_QUERY,
    CMD_TUNER_FREQ_QUERY,
    CMD_VOLUME,
    CMD_VOLUME_DOWN,
    CMD_VOLUME_QUERY,
    CMD_VOLUME_UP,
    COMMAND_PAUSE,
    COMMAND_TERMINATOR,
    DEFAULT_LISTENING_MODES,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SOURCES,
    DEFAULT_TIMEOUT,
    DOMAIN,
    LISTENING_MODE_ALIASES,
    LISTENING_MODE_CODE_MAPPING,
    MAX_SOURCE_SLOTS,
    MAX_RETRIES,
    RETRY_DELAY,
    SOURCE_ALIASES,
    SCAN_INTERVAL,
    SUPPORT_PIONEER,
    UPDATE_TIMEOUT,
    VOLUME_DB_OFFSET,
    VOLUME_MAX,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pioneer AVR LX83 media player."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data.get(CONF_PORT, DEFAULT_PORT)
    name = config_entry.data.get(CONF_NAME, DEFAULT_NAME)

    entity = PioneerAVR(hass, name, host, port)
    async_add_entities([entity], True)

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        "send_raw_command",
        cv.make_entity_service_schema({vol.Required("command"): cv.string}),
        "async_send_raw_command",
    )


class PioneerAVR(MediaPlayerEntity):
    """Representation of a Pioneer AVR LX83."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_icon = "mdi:amplifier"
    _attr_should_poll = True
    _attr_scan_interval = SCAN_INTERVAL

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        host: str,
        port: int,
    ) -> None:
        """Initialize the Pioneer AVR device."""
        self.hass = hass
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
        self._power_state = STATE_OFF
        self._playback_state: str | None = None
        self._volume = 0.0
        self._volume_step = 0
        self._is_muted = False
        self._source = None
        self._sources = dict(DEFAULT_SOURCES)
        self._source_code_to_name = {code: name for name, code in self._sources.items()}
        self._source_aliases = {
            name.lower(): code for name, code in self._sources.items()
        }
        self._source_aliases.update(SOURCE_ALIASES)
        self._sound_mode: str | None = None
        self._sound_mode_code: str | None = None
        self._sound_modes = dict(DEFAULT_LISTENING_MODES)
        self._sound_mode_code_to_name = {
            code: name for name, code in self._sound_modes.items()
        }
        self._sound_mode_aliases = {
            name.lower(): code for name, code in self._sound_modes.items()
        }
        self._sound_mode_aliases.update(LISTENING_MODE_ALIASES)
        self._tuner_frequency: float | None = None  # Frequency in MHz
        self._available = True
        self._retry_count = 0
        self._command_lock = asyncio.Lock()
        self._socket: socket.socket | None = None
        self._dynamic_sources_loaded = False

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return self._name

    @property
    def state(self) -> str:
        """Return the state of the device."""
        if self._power_state == STATE_OFF:
            return STATE_OFF
        return self._playback_state or STATE_ON

    @property
    def volume_level(self) -> float:
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def is_volume_muted(self) -> bool:
        """Boolean if volume is currently muted."""
        return self._is_muted

    @property
    def source(self) -> str | None:
        """Return the current input source."""
        return self._source

    @property
    def source_list(self) -> list[str]:
        """List of available input sources."""
        return list(self._sources.keys())

    @property
    def sound_mode(self) -> str | None:
        """Return current listening mode."""
        return self._sound_mode

    @property
    def sound_mode_list(self) -> list[str] | None:
        """List available listening modes."""
        if not self._sound_modes:
            return None
        return list(self._sound_modes.keys())

    @property
    def supported_features(self) -> int:
        """Flag media player features that are supported."""
        return SUPPORT_PIONEER

    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return self._available

    @property
    def extra_state_attributes(self) -> dict[str, float | int | str | list[str]]:
        """Expose raw Pioneer volume step and approximate dB."""
        attrs = {
            "volume_step": self._volume_step,
            "volume_db": self._step_to_db(self._volume_step),
            "sound_mode_code": self._sound_mode_code,
            "available_sound_modes": self.sound_mode_list,
        }
        if self._tuner_frequency is not None:
            attrs["tuner_frequency_mhz"] = self._tuner_frequency
        return attrs

    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        await self._send_command(CMD_POWER_ON)
        self._power_state = STATE_ON
        self._playback_state = None
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn off media player."""
        await self._send_command(CMD_POWER_OFF)
        self._power_state = STATE_OFF
        self._playback_state = None
        self.async_write_ha_state()

    async def async_volume_up(self) -> None:
        """Volume up media player."""
        await self._send_command(CMD_VOLUME_UP)
        # Mise à jour approximative du volume pour feedback immédiat
        self._volume_step = self._clamp_volume_step(self._volume_step + 1)
        self._volume = self._step_to_level(self._volume_step)
        self.async_write_ha_state()

    async def async_volume_down(self) -> None:
        """Volume down media player."""
        await self._send_command(CMD_VOLUME_DOWN)
        # Mise à jour approximative du volume pour feedback immédiat
        self._volume_step = self._clamp_volume_step(self._volume_step - 1)
        self._volume = self._step_to_level(self._volume_step)
        self.async_write_ha_state()

    async def async_media_play(self) -> None:
        """Send play command."""
        await self._send_command(CMD_MEDIA_PLAY)
        if self._power_state != STATE_OFF:
            self._playback_state = STATE_PLAYING
            self.async_write_ha_state()

    async def async_media_pause(self) -> None:
        """Send pause command."""
        await self._send_command(CMD_MEDIA_PAUSE)
        if self._power_state != STATE_OFF:
            self._playback_state = STATE_PAUSED
            self.async_write_ha_state()

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        volume_int = self._clamp_volume_step(int(volume * VOLUME_MAX))
        await self._send_command(f"{volume_int:03d}{CMD_VOLUME}")
        self._volume_step = volume_int
        self._volume = self._step_to_level(volume_int)
        self.async_write_ha_state()

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute (true) or unmute (false) media player."""
        if mute:
            await self._send_command(CMD_MUTE_ON)
        else:
            await self._send_command(CMD_MUTE_OFF)
        self._is_muted = mute
        self.async_write_ha_state()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        _LOGGER.debug("Selecting source: %s", source)
        resolved = self._resolve_source_code(source)
        if not resolved:
            _LOGGER.warning("Unknown source '%s' requested", source)
            return

        source_code, canonical_name = resolved
        _LOGGER.debug("Resolved source '%s' to code '%s' (%s)", source, source_code, canonical_name)
        await self._send_command(f"{source_code}{CMD_SOURCE}")
        self._source = canonical_name
        self.async_write_ha_state()

    async def async_select_sound_mode(self, sound_mode: str) -> None:
        """Select listening mode (sound mode)."""
        resolved = self._resolve_sound_mode(sound_mode)
        if not resolved:
            _LOGGER.debug("Unknown sound mode '%s' requested", sound_mode)
            return

        mode_code, canonical_name = resolved
        await self._send_command(f"{mode_code}{CMD_LISTENING_MODE}")
        self._sound_mode_code = mode_code
        self._sound_mode = canonical_name
        self.async_write_ha_state()
        # Rafraîchir l'état pour obtenir la réponse réelle de l'amplificateur
        await self.async_update()

    async def async_send_raw_command(self, command: str) -> None:
        """Expose a raw telnet command for advanced cards."""
        await self._send_command(command)

    async def async_update(self) -> None:
        """Get the latest details from the device."""
        # Use a global timeout to prevent exceeding scan interval
        # Allow up to 90% of scan interval to account for overhead
        max_update_time = SCAN_INTERVAL.total_seconds() * 0.9
        
        try:
            await asyncio.wait_for(
                self._async_update_internal(), timeout=max_update_time
            )
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Update took longer than %.1f seconds, aborting to avoid exceeding scan interval",
                max_update_time,
            )
            self._retry_count += 1
            if self._retry_count > MAX_RETRIES:
                self._available = False
        except Exception as err:
            _LOGGER.error("Error updating Pioneer AVR: %s", err)
            self._retry_count += 1
            if self._retry_count > MAX_RETRIES:
                self._available = False

    async def _async_update_internal(self) -> None:
        """Internal update logic without timeout wrapper."""
        # Query power state with shorter timeout for updates
        power_response = await self._send_command_with_response(
            CMD_POWER_QUERY, UPDATE_TIMEOUT
        )
        if power_response:
            # Vérifier les deux formats possibles de réponse
            self._power_state = (
                STATE_ON
                if (b"PWR0" in power_response or b"PWR2" in power_response)
                else STATE_OFF
            )
            if self._power_state == STATE_OFF:
                self._playback_state = None
            self._available = True
            self._retry_count = 0  # Reset retry count on successful update
        else:
            self._retry_count += 1
            if self._retry_count > MAX_RETRIES:
                self._available = False
            return

        if self._power_state == STATE_ON:
            # Load dynamic sources only once, and don't block updates if it fails
            if not self._dynamic_sources_loaded:
                try:
                    await asyncio.wait_for(
                        self._ensure_dynamic_sources(), timeout=UPDATE_TIMEOUT * 5
                    )
                except asyncio.TimeoutError:
                    _LOGGER.warning(
                        "Dynamic sources discovery timed out, continuing with default sources"
                    )
                    self._dynamic_sources_loaded = True  # Mark as loaded to avoid retrying
                except Exception as err:
                    _LOGGER.debug("Error loading dynamic sources: %s", err)
                    self._dynamic_sources_loaded = True  # Mark as loaded to avoid retrying

            # Query volume with shorter timeout
            volume_response = await self._send_command_with_response(
                CMD_VOLUME_QUERY, UPDATE_TIMEOUT
            )
            if volume_response:
                try:
                    vol_str = volume_response.decode().strip()
                    # Chercher tous les chiffres après "VOL"
                    if "VOL" in vol_str:
                        vol_value = int(vol_str.replace("VOL", ""))
                        self._volume_step = vol_value
                        self._volume = self._step_to_level(vol_value)
                except (ValueError, AttributeError, UnicodeDecodeError) as err:
                    _LOGGER.debug("Error parsing volume response: %s", err)

            # Query mute state with shorter timeout
            mute_response = await self._send_command_with_response(
                CMD_MUTE_QUERY, UPDATE_TIMEOUT
            )
            if mute_response:
                try:
                    mute_str = mute_response.decode().strip()
                    self._is_muted = "MUT0" in mute_str
                except (UnicodeDecodeError, AttributeError) as err:
                    _LOGGER.debug("Error parsing mute response: %s", err)

            # Query source with shorter timeout
            source_response = await self._send_command_with_response(
                CMD_SOURCE_QUERY, UPDATE_TIMEOUT
            )
            if source_response:
                try:
                    src_str = source_response.decode().strip()
                    if "FN" in src_str:
                        src_code = src_str.split("FN", 1)[1].strip()
                        self._source = self._name_for_code(src_code)
                except (UnicodeDecodeError, AttributeError) as err:
                    _LOGGER.debug("Error parsing source response: %s", err)

            # Query listening mode with shorter timeout
            mode_response = await self._send_command_with_response(
                CMD_LISTENING_MODE_QUERY, UPDATE_TIMEOUT
            )
            self._update_sound_mode_from_response(mode_response)

            # Query tuner frequency if source is Tuner
            if self._source == "Tuner":
                freq_response = await self._send_command_with_response(
                    CMD_TUNER_FREQ_QUERY, UPDATE_TIMEOUT
                )
                if freq_response:
                    try:
                        freq_str = freq_response.decode().strip()
                        # Format Pioneer: "FR12345" where 12345 = 123.45 MHz
                        # 5 digits: first 3 are MHz, last 2 are decimals
                        if "FR" in freq_str:
                            freq_raw = freq_str.replace("FR", "").strip()
                            if freq_raw and freq_raw.isdigit():
                                # Parse as integer (e.g., 12345) and convert to MHz (123.45)
                                freq_int = int(freq_raw)
                                self._tuner_frequency = freq_int / 100.0
                            else:
                                self._tuner_frequency = None
                        else:
                            self._tuner_frequency = None
                    except (ValueError, UnicodeDecodeError, AttributeError) as err:
                        _LOGGER.debug("Error parsing tuner frequency response: %s", err)
                        self._tuner_frequency = None
                else:
                    self._tuner_frequency = None
            else:
                self._tuner_frequency = None

    async def async_will_remove_from_hass(self) -> None:
        """Close TCP connection when entity is removed."""
        await super().async_will_remove_from_hass()
        await self.hass.async_add_executor_job(self._close_socket)

    async def _ensure_dynamic_sources(self) -> None:
        """Discover source labels reported by the AVR."""
        if self._dynamic_sources_loaded:
            return

        consecutive_misses = 0
        for idx in range(MAX_SOURCE_SLOTS):
            code = f"{idx:02d}"
            # Use shorter timeout for source discovery to avoid blocking
            response = await self._send_command_with_response(
                f"{CMD_SOURCE_NAME_QUERY}{code}", UPDATE_TIMEOUT
            )
            if not response:
                consecutive_misses += 1
                if consecutive_misses >= 10:
                    break
                continue

            consecutive_misses = 0
            try:
                raw = response.decode().strip()
            except UnicodeDecodeError:
                continue

            if not raw.startswith("RGB") or len(raw) <= 5:
                continue

            label = raw[5:].strip()
            if not label:
                continue

            self._register_source(label, code)

        self._dynamic_sources_loaded = True

    def _register_source(self, name: str, code: str) -> None:
        """Store a source label/code pair if not already known."""
        clean_name = name.strip()
        clean_code = code.strip()
        if not clean_name or not clean_code:
            return
        if clean_name not in self._sources:
            self._sources[clean_name] = clean_code
        self._source_code_to_name.setdefault(clean_code, clean_name)
        self._source_aliases[clean_name.lower()] = clean_code

    def _resolve_source_code(self, label: str) -> tuple[str, str] | None:
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

    def _name_for_code(self, code: str) -> str:
        """Return a friendly label for a source code."""
        clean_code = code.strip()
        if not clean_code:
            return clean_code
        if clean_code in self._source_code_to_name:
            return self._source_code_to_name[clean_code]
        fallback = f"Input {clean_code}"
        self._register_source(fallback, clean_code)
        return fallback

    def _resolve_sound_mode(self, label: str) -> tuple[str, str] | None:
        """Return (code, canonical_name) for a listening mode."""
        if not label:
            return None
        clean_label = label.strip()
        if not clean_label:
            return None
        if clean_label in self._sound_modes:
            return self._sound_modes[clean_label], clean_label
        lowered = clean_label.lower()
        alias_code = self._sound_mode_aliases.get(lowered)
        if alias_code:
            canonical = self._sound_mode_code_to_name.get(
                alias_code, self._name_for_sound_mode_code(alias_code)
            )
            return alias_code, canonical
        return None

    def _name_for_sound_mode_code(self, code: str) -> str:
        """Return a friendly label for a listening mode code."""
        clean_code = code.strip()
        if not clean_code:
            return clean_code
        clean_code = clean_code.zfill(4)
        if clean_code in self._sound_mode_code_to_name:
            return self._sound_mode_code_to_name[clean_code]
        fallback = f"Mode {clean_code}"
        self._sound_mode_code_to_name[clean_code] = fallback
        if fallback not in self._sound_modes:
            self._sound_modes[fallback] = clean_code
        self._sound_mode_aliases[fallback.lower()] = clean_code
        return fallback

    def _update_sound_mode_from_response(self, response: bytes | None) -> None:
        """Parse listening mode feedback.
        
        Format de réponse attendu: "LM0001", "LM0006", "LM0401", "LM0208", "LM0056", etc.
        Certains modèles retournent des codes étendus (ex: "0401" pour Auto Surround, "0208" pour Advanced Game).
        Pour THX Cinema, certains modèles peuvent retourner "LM56", "LM056", "LM0056", "LM0506", etc.
        Ces codes sont mappés vers les codes standards via LISTENING_MODE_CODE_MAPPING.
        """
        if not response:
            return
        try:
            raw = response.decode().strip()
        except (UnicodeDecodeError, AttributeError):
            return
        
        code = None
        
        # Chercher le pattern "LM" suivi de chiffres
        if "LM" in raw:
            lm_index = raw.find("LM")
            if lm_index != -1:
                after_lm = raw[lm_index + 2:]  # Tout après "LM"
                digits = "".join(ch for ch in after_lm if ch.isdigit())
                if len(digits) >= 4:
                    # Prendre les 4 premiers chiffres après "LM"
                    code = digits[:4].zfill(4)
                elif len(digits) > 0:
                    # Certains modèles retournent moins de 4 chiffres (ex: "LM56" pour THX Cinema)
                    # Essayer de mapper directement le code court
                    code_short = digits.zfill(4)  # "56" -> "0056"
                    # Vérifier aussi sans padding pour le mapping
                    code_raw = digits
                    # Essayer de mapper le code court d'abord
                    if code_raw in LISTENING_MODE_CODE_MAPPING:
                        code = LISTENING_MODE_CODE_MAPPING[code_raw].zfill(4)
                    elif code_short in LISTENING_MODE_CODE_MAPPING:
                        code = LISTENING_MODE_CODE_MAPPING[code_short].zfill(4)
                    else:
                        code = code_short
        
        # Fallback: chercher des chiffres dans la réponse
        if not code:
            digits = "".join(ch for ch in raw if ch.isdigit())
            if len(digits) >= 4:
                code = digits[:4].zfill(4)
            elif len(digits) > 0:
                # Essayer de mapper le code court
                code_raw = digits
                if code_raw in LISTENING_MODE_CODE_MAPPING:
                    code = LISTENING_MODE_CODE_MAPPING[code_raw].zfill(4)
                else:
                    code = digits.zfill(4)
        
        if not code:
            _LOGGER.warning("Could not parse listening mode from response: %s", raw)
            return
        
        # Mapper le code étendu vers le code standard si nécessaire
        # Essayer d'abord avec le code tel quel, puis avec différentes longueurs
        standard_code = LISTENING_MODE_CODE_MAPPING.get(code, code)
        if standard_code == code:  # Pas de mapping trouvé, essayer avec code court
            code_short = code.lstrip('0')  # "0056" -> "56"
            if code_short and code_short != code:
                standard_code = LISTENING_MODE_CODE_MAPPING.get(code_short, code)
                if standard_code != code_short:
                    standard_code = standard_code.zfill(4)
        
        # Utiliser le code standard pour la recherche du nom
        self._sound_mode_code = standard_code
        self._sound_mode = self._name_for_sound_mode_code(standard_code)
        _LOGGER.debug("Parsed listening mode: %s -> raw code: %s -> standard code: %s -> name: %s", 
                     raw, code, standard_code, self._sound_mode)

    async def _send_command(self, command: str) -> None:
        """Send a command to the Pioneer AVR."""
        async with self._command_lock:
            try:
                await self.hass.async_add_executor_job(self._send_command_sync, command)
            except (
                socket.timeout,
                socket.error,
                ConnectionRefusedError,
                OSError,
            ) as err:
                _LOGGER.error("Network error sending command '%s': %s", command, err)
                self._retry_count += 1
                if self._retry_count > MAX_RETRIES:
                    self._available = False
            except Exception as err:
                _LOGGER.error("Error sending command '%s': %s", command, err)
                self._retry_count += 1
                if self._retry_count > MAX_RETRIES:
                    self._available = False

    async def _send_command_with_response(
        self, command: str, timeout: float | None = None
    ) -> bytes | None:
        """Send a command and get response."""
        async with self._command_lock:
            try:
                return await self.hass.async_add_executor_job(
                    self._send_command_sync_with_response, command, timeout
                )
            except (
                socket.timeout,
                socket.error,
                ConnectionRefusedError,
                OSError,
            ) as err:
                _LOGGER.error("Network error sending command '%s': %s", command, err)
                self._retry_count += 1
                if self._retry_count > MAX_RETRIES:
                    self._available = False
                return None
            except Exception as err:
                _LOGGER.error("Error sending command '%s': %s", command, err)
                self._retry_count += 1
                if self._retry_count > MAX_RETRIES:
                    self._available = False
                return None

    def _send_command_sync(self, command: str) -> None:
        """Send command synchronously with retry."""
        payload = self._build_payload(command)
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                sock = self._ensure_socket()
                sock.sendall(payload)
                time.sleep(COMMAND_PAUSE)
                return
            except (
                socket.timeout,
                socket.error,
                ConnectionRefusedError,
                OSError,
            ) as err:
                _LOGGER.error(
                    "Error sending command '%s' to %s:%s (attempt %d/%d): %s",
                    command,
                    self._host,
                    self._port,
                    attempt,
                    MAX_RETRIES,
                    err,
                )
                self._close_socket()
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                else:
                    raise

    def _send_command_sync_with_response(
        self, command: str, timeout: float | None = None
    ) -> bytes:
        """Send command and get response synchronously with retry."""
        payload = self._build_payload(command)
        used_timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                sock = self._ensure_socket(used_timeout)
                sock.sendall(payload)
                time.sleep(COMMAND_PAUSE)
                return self._read_response(sock, used_timeout)
            except (
                socket.timeout,
                socket.error,
                ConnectionRefusedError,
                OSError,
            ) as err:
                _LOGGER.error(
                    "Error sending command '%s' with response to %s:%s (attempt %d/%d): %s",
                    command,
                    self._host,
                    self._port,
                    attempt,
                    MAX_RETRIES,
                    err,
                )
                self._close_socket()
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                else:
                    raise

    def _clamp_volume_step(self, step: int) -> int:
        """Ensure the raw volume step stays within Pioneer limits."""
        return max(0, min(VOLUME_MAX, step))

    def _ensure_socket(self, timeout: float | None = None) -> socket.socket:
        """Return an active socket connection, opening it if needed."""
        used_timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        if self._socket is not None:
            # Update timeout on existing socket if different
            if timeout is not None:
                self._socket.settimeout(used_timeout)
            return self._socket

        sock = socket.create_connection(
            (self._host, self._port), timeout=used_timeout
        )
        sock.settimeout(used_timeout)
        self._socket = sock
        return sock

    def _close_socket(self) -> None:
        """Close the reusable socket, ignoring errors."""
        if self._socket is None:
            return
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self._socket.close()
        except OSError:
            pass
        self._socket = None

    def _build_payload(self, command: str) -> bytes:
        """Return the raw bytes to send for a Pioneer telnet command."""
        return (command + COMMAND_TERMINATOR).encode()

    def _read_response(self, sock: socket.socket, timeout: float | None = None) -> bytes:
        """Read bytes from the AVR until a terminator or timeout is reached."""
        response = b""
        used_timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        deadline = time.monotonic() + used_timeout
        terminator = COMMAND_TERMINATOR.encode()

        while time.monotonic() < deadline:
            try:
                chunk = sock.recv(1024)
            except socket.timeout:
                break
            except OSError:
                self._close_socket()
                break

            if not chunk:
                self._close_socket()
                break

            response += chunk

            if terminator in response or b"\n" in response:
                break

        return response

    def _step_to_level(self, step: int) -> float:
        """Convert Pioneer step (0-185) to HA 0..1 scale."""
        return step / VOLUME_MAX

    def _step_to_db(self, step: int) -> float:
        """Convert Pioneer step to approximate dB shown on AVR in relative mode."""
        return step - VOLUME_DB_OFFSET
