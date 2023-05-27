"""Support for Plex webhooks."""
from __future__ import annotations

import aiofiles
import aiohttp
import logging
import os

from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_RECEIVED, THUMBNAIL_DIRECTORY

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the Plex Webhooks component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure based on config entry."""
    webhook.async_register(
        hass, DOMAIN, "Plex", entry.data[CONF_WEBHOOK_ID], handle_webhook,
    )
    if not os.path.isdir(THUMBNAIL_DIRECTORY):
        os.mkdir(THUMBNAIL_DIRECTORY)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])
    return True


async_remove_entry = config_entry_flow.webhook_async_remove_entry


async def handle_webhook(
    hass: HomeAssistant,
    webhook_id: str,
    request: aiohttp.web.Request,
) -> None:
    """Handle incoming webhook with Plex inbound messages."""
    _LOGGER.debug(f"Received message - webhook_id: {webhook_id}")

    data = {}
    try:
        reader = await request.multipart()
        while True:
            part = await reader.next()
            if part is None:
                break
            if part.headers[aiohttp.hdrs.CONTENT_TYPE] == "application/json":
                data = await part.json()
                continue
            async with aiofiles.open(
                file=f"{THUMBNAIL_DIRECTORY}/{webhook_id}.png",
                mode="wb",
            ) as file:
                await file.write(await part.read(decode=False))
    except ValueError:
        _LOGGER.warn(f"Issue decoding webhook: {part.text()}")
        return

    data["webhook_id"] = webhook_id
    hass.bus.async_fire(EVENT_RECEIVED, data)
    return
