import logging
import os
from flask import Flask, request, jsonify
from bot.fb_handle import  out_server_to_in_nlp
from bot.bot_fb import Bot as BotFB
from bot.bot import InfoBotFb
from dto.response import BaseResponse
from handler.exception_handler import bad_request_exception_handler, internal_server_error_handler
from werkzeug.exceptions import BadRequest, InternalServerError
from config import config

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
app = Flask(__name__)
app.register_error_handler(BadRequest, bad_request_exception_handler)
app.register_error_handler(InternalServerError, internal_server_error_handler)


@app.route('/', methods=['GET', 'POST'])
def index():
    res = BaseResponse(code=200, res="ok", des="service is running")
    return jsonify(res.__dict__), 200


@app.route('/integration/webhook/fb/', methods=['GET'])
def fb_verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == config.fb_verify_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "ok", 200


@app.route('/integration/webhook/fb', methods=['POST'])
def fb_webhook():
    data = request.get_json()
    welcome = "Hướng dẫn đăng ký và huỷ nhận thông báo:\n- Đăng ký: \n DK <Tài khoản> <Mật khẩu>  " \
                "\n Ví dụ: DK IC01_009 123456\n- Hủy: \n HUY <Tài khoản>  \n Ví dụ: HUY IC01_009"
    try:
        bot_model = InfoBotFb(bot_id=config.bot_id, channel="facebook",
                              token=config.token, page_id=config.page_id).__dict__

        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # option confirmation
                        pass
                    if messaging_event.get("postback"):
                        in_nlp = out_server_to_in_nlp(messaging=messaging_event, bot=bot_model)
                        info = in_nlp.__dict__
                        sender_id = info["sender_id"]
                        if messaging_event["postback"]["title"] == "Get Started":
                            bot_fb = BotFB(config.token)
                            bot_fb.send_text_message(recipient_id=sender_id, message=welcome)

                    if messaging_event.get("message"):
                        in_nlp = out_server_to_in_nlp(messaging=messaging_event, bot=bot_model)
                        info = in_nlp.__dict__
                        bot_fb = BotFB(config.token)
                        bot_fb.send_text_message(recipient_id=info["sender_id"], message=info["text"])

    except Exception as e:
        logging.getLogger().exception("PROCESSING FB WEBHOOK ERROR: {}".format(str(e)))
    return "ok", 200


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0", port=int(config.service_port))
