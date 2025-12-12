"""Config flow for Pioneer AVR LX83 integration."""
from __future__ import annotations

import logging
from typing import Any
import telnetlib

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DEFAULT_NAME, DEFAULT_PORT, DEFAULT_TIMEOUT, DOMAIN

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
            tn.write(b"?P\n")
            response = tn.read_until(b"\n", timeout=DEFAULT_TIMEOUT)
            return True
    except Exception as err:
        _LOGGER.error("Connection test failed: %s", err)
        raise


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pioneer AVR LX83."""

    VERSION = 1

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
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

