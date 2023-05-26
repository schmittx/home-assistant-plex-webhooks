"""Support for Plex webhooks."""
from __future__ import annotations

from aiohttp.web import Request
import logging

from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLEX_EVENT

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the Plex Webhooks component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure based on config entry."""
    webhook.async_register(
        hass, DOMAIN, "Plex", entry.data[CONF_WEBHOOK_ID], handle_webhook,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])
    return True


async_remove_entry = config_entry_flow.webhook_async_remove_entry


async def handle_webhook(hass: HomeAssistant, webhook_id: str, request: Request) -> None:
    """Handle incoming webhook with Plex inbound messages."""
    _LOGGER.debug(
        "Plex webook received message - webhook_id: %s",
        webhook_id,
    )

    data = {}
    try:
        reader = await request.multipart()
        # https://docs.aiohttp.org/en/stable/multipart.html#aiohttp-multipart
        while True:
            part = await reader.next()
            if part is None:
                break
            if part.name == "payload":
                data = await part.json()
    except ValueError:
        _LOGGER.warn("Issue decoding webhook: " + part.text())
        return None

    data["webhook_id"] = webhook_id
    hass.bus.async_fire(PLEX_EVENT, data)
    return
