[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
# Plex Webhooks Home Assistant Integration
Custom component to handle [Plex webhooks](https://support.plex.tv/articles/115002267687-webhooks/) in [Home Assistant](https://home-assistant.io).

## Credit
- [@JBassett's plex_webhooks project](https://github.com/JBassett/plex_webhooks) - Initial Home Assistant component

## Install
1. Ensure Home Assistant is updated to version 2025.2.0 or newer.
2. Use HACS and add as a [custom repo](https://hacs.xyz/docs/faq/custom_repositories); or download and manually move to the `custom_components` folder.
3. Once the integration is installed follow the standard process to setup via UI and search for `Plex Webhooks`.
4. Follow the prompts.
5. Make note of the web hook URL

## Set up the webhook in Plex

As an administrator of Plex, go to the Webhooks page, and add the URL from Step 5 above.

_NOTE: adding a Webhook in Plex requires a 'Plex Pass'._

## Actions of the Integration

When a Webhook call is received from Plex, this integration will do the following:

1. Publish an Event to the [Home Assistant Event bus](https://www.home-assistant.io/docs/configuration/events/).
1. _[Optionally - if the event relates to a media item]_ A thumbnail image will be saved to the the `/www/plex_webhooks` folder.


## ✨Tip: Testing out the integration

It's possible to see the raw details of a Plex Webhook event by utilizing the `Developer Tools` section of Home Assistant.

Go to `Developer Tools`, and the select the `Events` tab. In the `Listen to event` section, enter `plex_webhooks_received` in the `Events to subscribe to` input, then click the `Start listening` button.

From here, do something which will emit a Webhook call in Plex, and you will see the event logged in the Event log.

This can be a great aid to working out the `Player.uuid` of your device(s)!


## Using this Integration in an Automation

If you would like to set up an Automation to react to Webhook calls, carry out the following steps:

1. Create a new Automation
1. Select `Manual event` as the trigger.
1. For the `Event type`, use: `plex_webhooks_received`

The Plex [web hook payload](https://support.plex.tv/articles/115002267687-webhooks/#toc-2) is available on the event path of `trigger.event.data` within the automation. Generally you will be interested in 2 elements of the data: the event type, and (possibly) the device (Player) which initiated the event. 

### Example:

To trigger an event when someone starts to 'Play' an item on a specific player:

#### When:
```
Event 'plex_webhooks_received' is received
```

#### And if:
```
{{trigger.event.data.event == 'media.play'}}
&
{{trigger.event.data.Player.uuid == 'xxxyyyzzz-your-player-id'}}
```
#### Then do:
```
Go wild!
```
