"""Config flow for Pioneer AVR LX83 integration."""
from __future__ import annotations

import logging
import telnetlib
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_SOURCES,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SOURCES,
    DEFAULT_TIMEOUT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    host = data[CONF_HOST]
    port = data[CONF_PORT]

    try:
        # Test connection
        await hass.async_add_executor_job(_test_connection, host, port)
    except Exception as err:
        _LOGGER.error("Cannot connect to Pioneer AVR: %s", err)
        raise CannotConnect from err

    return {"title": data[CONF_NAME]}


def _test_connection(host: str, port: int) -> bool:
    """Test if we can connect to the device."""
    try:
        with telnetlib.Telnet(host, port, timeout=DEFAULT_TIMEOUT) as tn:
            tn.write(b"?P\r\n")
            response = tn.read_until(b"\r\n", timeout=DEFAULT_TIMEOUT)
            if not response:
                raise ConnectionError("No response from device")
            return True
    except (OSError, ConnectionError, TimeoutError) as err:
        _LOGGER.error("Connection test failed to %s:%s: %s", host, port, err)
        raise
    except Exception as err:
        _LOGGER.error("Unexpected error during connection test: %s", err)
        raise


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pioneer AVR LX83."""

    VERSION = 1

    @staticmethod
    async def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "unknown"
            else:
                unique_id = f"{user_input[CONF_HOST]}_{user_input.get(CONF_PORT, DEFAULT_PORT)}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                # Add default sources to options
                user_input.setdefault(CONF_SOURCES, DEFAULT_SOURCES)
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_import(self, import_info: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_info)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Pioneer AVR LX83."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Update sources if provided
            current_sources = self.config_entry.data.get(CONF_SOURCES, DEFAULT_SOURCES)
            # For now, we just return - sources customization can be added later
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

