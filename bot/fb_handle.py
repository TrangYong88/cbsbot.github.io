from typing import List
import logging
from bot.bot import InputNLP, MsgInfo
from bot.bot_fb import Bot as BotFB


def processing_fb_data_checkin(bot: dict, data: object):
    try:
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
                    if messaging_event.get("message") or messaging_event.get("postback"):
                        in_nlp = out_server_to_in_nlp(messaging=messaging_event, bot=bot)
                        info = in_nlp.__dict__
                        new_info = MsgInfo(bot_id=info["bot_id"], user_id=info["sender_id"],
                                           text=info["text"], channel=info["input_channel"]).__dict__
                        return new_info

    except Exception as e:
        logging.getLogger().exception("processing fb data error: {}".format(e))


def processing_fb_data(bot: dict, res: object) -> None:
    try:
        handle_output_nlp(bot, res)
    except Exception as e:
        logging.getLogger().exception("processing fb data error: {}".format(str(e)))


def out_server_to_in_nlp(messaging: object, bot: dict) -> InputNLP:
    in_nlp = InputNLP()
    in_nlp.bot_id = bot["bot_id"]
    in_nlp.input_channel = "facebook"

    if messaging.get("message") is not None:
        in_nlp.sender_id = messaging["sender"]["id"]  # the facebook ID of the person sending you the message
        if messaging.get("message").get("quick_reply"):
            in_nlp.text = messaging["message"]["quick_reply"]["payload"]
        else:  # msg is text
            in_nlp.text = messaging["message"]["text"]  # the message's text

    if messaging.get("postback") is not None:
        in_nlp.sender_id = messaging["sender"]["id"]  # the facebook ID of the person sending you the message
        in_nlp.text = messaging["postback"]["payload"]
    return in_nlp


def handle_output_nlp(bot: dict, out_nlp: object) -> None:
    bot_fb = BotFB(bot["token"])
    for card in out_nlp["card_data"]:
        if card['type'] == 'text' and card['text'] != "":  # TODO: send text_card
            if len(card['buttons']) == 0:
                bot_fb.send_text_message(recipient_id=out_nlp['userId'], message=card['text'])

            else:
                buttons = buttons_format(card["buttons"])
                bot_fb.send_button_message(recipient_id=out_nlp["userId"], text=card["text"], buttons=buttons)

        elif card['type'] == 'image':  # TODO: send image_card
            if len(card["buttons"]) == 0:  # send only image
                elements = []
                element = {"title": card["title"], "subtitle": card["subtitle"],
                           "image_url": card["url"]}
                elements.append(element)  # TODO: Con co default action nua
                bot_fb.send_generic_message(recipient_id=out_nlp["userId"], elements=elements)

            else:
                buttons = buttons_format(card["buttons"])
                elements = []
                element = {"title": card["title"], "subtitle": card["subtitle"],
                           "image_url": card["url"], "buttons": buttons}
                elements.append(element)  # TODO: Con co default action nua
                bot_fb.send_generic_message(recipient_id=out_nlp["userId"], elements=elements)


def buttons_format(buttons: List[object]) -> List[object]:
    btns = []
    for b in buttons:
        if b["type"] == "postback":  # button is postback
            button = {"type": "postback", "title": b["title"], "payload": b["payload"]}
            btns.append(button)
        elif b["type"] == "web_url":  # button is link web
            button = {"type": "web_url", "url": b["payload"], "title": b["title"]}
            btns.append(button)
        elif b["type"] == "phone_number":  # button is phonenumber
            button = {"type": "phone_number", "title": b["title"], "payload": b["payload"]}
            btns.append(button)
    return btns

