import datetime
import json
import logging
import random
from uuid import uuid4
from config import config
import requests


def main(config):
    random.seed(config["seed"])
    some_date = random_date()
    return some_date


def random_date():
    earliest = datetime.date(2020, 5, 1)
    latest = datetime.date(2020, 5, 10)
    delta = latest - earliest
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    a = str(earliest + datetime.timedelta(seconds=random_second)  )
    return a


class Bot:
    def __init__(self, bot_id: str, token: str, channel: str) -> None:
        self.bot_id = bot_id
        self.token = token
        self.channel = channel


class InputNLP:
    def __init__(self):
        self.bot_id = None
        self.sender_id = None
        self.text = None
        self.input_channel = None


class OutNLP:
    def __init__(self):
        pass


class ChatLogs:
    def __init__(self):
        self.id = str(uuid4())
        self.bot_id = None
        self.sender_id = None
        self.message = None
        self.source = None  # bot, admin, client
        self.input_channel = None  # fb, tele, zalo, viber, livechat
        self.add_info = None
        self.created_time = datetime.datetime.now()


class InfoPredict:
    def __init__(self):
        self.id = str(uuid4())
        self.bot_id = None
        self.text = None
        self.intent_confidence = None
        self.intent_name = None
        self.step = None
        self.nlu_threshold = None
        self.sender_id = None
        self.result_data = None
        self.source = None  # 1: call nlu (proxy), 2: call action
        self.created_time = datetime.datetime.now()

        self.last_updated_time = self.created_time
        self.id_chatlog = None
        self.status_delete = None
        self.updated_intent = None
        self.len_card_data = None


class InfoStep:
    def __init__(self):
        self.id = None
        self.id_bot_predict = None
        self.step = None


class InfoChat:
    def __init__(self):
        self.id = uuid4()
        self.bot_id = None
        self.text = None
        self.intent_confidence = 0.1
        self.intent_name = None
        self.step = None
        self.nlu_threshold = 0.1
        self.sender_id = None
        self.result_data = None
        self.source = None
        self.created_time = datetime.datetime.now()
        self.last_updated_time = self.created_time
        self.add_info = None
        self.input_channel = None
        self.status_delete = None
        self.updated_intent = None
        self.len_card_data = 1


class MsgInfo:
    def __init__(self, bot_id='abc', user_id='', text='abc', channel='telegram'):
        self.botId = bot_id
        self.userId = user_id
        self.text = text
        self.channel = channel


class InfoBotFb:
    def __init__(self, bot_id='abc', channel='facebook', token='', page_id=''):
        self.bot_id = bot_id
        self.channel = channel
        self.token = token
        self.page_id = page_id

