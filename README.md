# home-assistant-plex-webhooks
Plex Webhooks integration for Home Assistant


[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
# Plex Webhooks Home Assistant Integration
Custom component to handle [Plex webhooks](https://support.plex.tv/articles/115002267687-webhooks/) in [Home Assistant](https://home-assistant.io).

## Credit
- [@JBassett's plex_webhooks project](https://github.com/JBassett/plex_webhooks) - Initial Home Assistant component

## Notes
- Some webhooks includes a thumbnail image. When present, this is parsed and saved to `/www/plex_webhooks` folder for use.

## Install
1. Ensure Home Assistant is updated to version 2021.4.0 or newer.
2. Use HACS and add as a [custom repo](https://hacs.xyz/docs/faq/custom_repositories); or download and manually move to the `custom_components` folder.
3. Once the integration is installed follow the standard process to setup via UI and search for `Plex Webhooks`.
4. Follow the prompts.
