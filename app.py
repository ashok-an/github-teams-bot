import json
import requests

import bot_utils
import cards
import settings
import search
import teams_sdk


import cr_list
import pr_list
import pr_details


def do_pr_list(userid, roomid):
    results = pr_list.get_pr_list(userid)
    card = cards.get_pr_list_output_card(userid, results)
    return teams_sdk.send_card_to_room(roomid, card)


def do_cr_list(userid, roomid):
    results = cr_list.get_cr_list(userid)
    card = cards.get_cr_list_output_card(userid, results)
    return teams_sdk.send_card_to_room(roomid, card)


def do_pr_details(pr_number, roomid):
    results = pr_details.get_pr_details(int(pr_number))
    card = cards.get_pr_details_output_card(pr_number, results)
    return teams_sdk.send_card_to_room(roomid, card)


def do_search(query_string, roomid):
    _results = search.search_engine(query_string)
    results = search.list_to_markdown(_results)
    card = cards.get_search_output_card(query_string, results)
    return teams_sdk.send_card_to_room(roomid, card)


def do_support(pr_number, support_string, roomid):
    return f'[todo] do_support({pr_number}, {support_string})'


# check attachmentActions:created webhook to handle any card actions 
def handle_cards(api, message):
    roomid = message.get("data", {}).get("roomId", 'no-room-id')
    actions = bot_utils.get_attachment_actions(message.get("data", {}).get("id", 'no-id'))
    if not actions:
        return

    if 'pr_list.user_id' in actions.keys():
        return do_pr_list(actions['pr_list.user_id'], roomid)
    elif 'cr_list.user_id' in actions.keys():
        return do_cr_list(actions['cr_list.user_id'], roomid)
    elif 'pr_details.pr_number' in actions.keys():
        return do_pr_details(actions['pr_details.pr_number'], roomid)
    elif 'query_string' in actions.keys():
        return do_search(actions['query_string'], roomid)
    elif 'support.details' in actions.keys():
        return do_support(actions['support.pr_number'], actions['support.details'], roomid)
    elif 'choice' in actions.keys():
        card, choice = None, actions['choice']
        if choice == 'pr_list':
            card = cards.get_pr_list_input_card()
        elif choice == 'cr_list':
            card = cards.get_cr_list_input_card()
        elif choice == 'pr_details':
            card = cards.get_pr_details_input_card()
        elif choice == 'search':
            card = cards.get_search_input_card()
        elif choice == 'support':
            card = cards.get_support_input_card()
        else:
            return f'Unknown choice: `{choice}`'

        if card:
            return teams_sdk.send_card_to_room(roomid, card)
    else:
        return f"Unknown action: `{actions}`"


def handle_menu(message):
    userid = message.personEmail.replace('@cisco.com', '')
    card = cards.get_menu_card()
    return teams_sdk.send_card_to_user(userid, card)


# Add new commands to the box.
bot_utils.bot.add_command("/menu", "show options", handle_menu)
bot_utils.bot.add_command('attachmentActions', '*', handle_cards)


if __name__ == "__main__":
    # Run Bot
    bot_utils.bot.run(host="0.0.0.0", port=9919, debug=True)
