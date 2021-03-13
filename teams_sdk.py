from webexteamssdk import WebexTeamsAPI
import settings

api = WebexTeamsAPI(access_token=settings.teams_token)

def get_me():
    return api.people.me()

def send_message_to_user(user_id, message):
    toEmail = user_id + '@cisco.com'
    api.messages.create(toPersonEmail=toEmail, markdown=message)
    return

def send_message_to_room(room_id, message):
    api.messages.create(roomId=room_id, markdown=message)
    return

def _wrap(card_obj):
    return {"contentType": "application/vnd.microsoft.card.adaptive", "content": card_obj.to_dict()}

def send_card_to_user(user_id, card_obj, fallback_message='card creation failed'):
    toEmail = user_id + '@cisco.com'
    api.messages.create(toPersonEmail=toEmail, attachments=[_wrap(card_obj),], text=fallback_message)
    return

def send_card_to_room(room_id, card_obj, fallback_message='card creation failed'):
    api.messages.create(roomId=room_id, attachments=[_wrap(card_obj),], text=fallback_message)
    return


if __name__ == '__main__':
    print(get_me())
