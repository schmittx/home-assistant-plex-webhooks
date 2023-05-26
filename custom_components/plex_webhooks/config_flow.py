"""Adds config flow for Plex Webhooks integration."""
from __future__ import annotations

from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    domain=DOMAIN,
    title="Plex Webhook",
    description_placeholder={
        "docs_url": "https://www.home-assistant.io/docs/configuration/events/",
        "plex_url": "https://support.plex.tv/articles/115002267687-webhooks/",
    },
    allow_multiple=True,
)
