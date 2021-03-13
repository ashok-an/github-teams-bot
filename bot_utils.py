import json
import requests

from webexteamsbot import TeamsBot

import settings


bot = TeamsBot(
    str(settings.bot_app_name),
    teams_bot_token=settings.teams_token,
    teams_bot_url=settings.bot_url,
    teams_bot_email=settings.bot_email,
    debug=True,
    webhook_resource_event=[{"resource": "messages", "event": "created"},
                            {"resource": "attachmentActions", "event": "created"}]
)


def get_attachment_actions(attachment_id):
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': 'Bearer ' + settings.teams_token
    }

    url = 'https://api.ciscospark.com/v1/attachment/actions/' + attachment_id
    response = requests.get(url, headers=headers)
    _json = response.json()
    return _json.get('inputs', {})


def split_message(message):
    tokens = message.text.split( )
    cmd = tokens.pop(0)
    return cmd, ' '.join(tokens).strip()

