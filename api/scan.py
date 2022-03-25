import time

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import json
import time
import asyncio


def get_info(number: str):
    with open("setting.json", 'r', encoding='utf8') as out:
        setting = json.load(out)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(
            setting['account']['session'],
            setting['account']['api_id'],
            setting['account']['api_hash'],
            loop=loop
        )
        client.start()
        bot = client.get_entity(setting['account']['target'])

        client.send_message(bot, number)
        time.sleep(0.5)
        while True:
            history = client(GetHistoryRequest(
                peer=bot,
                offset_id=0,
                offset_date=None, add_offset=0,
                limit=1, max_id=0, min_id=0,
                hash=0))
            print(history.messages[0].message)
            if "Расширенный поиск" in history.messages[0].message:
                break
            else:
                time.sleep(0.5)
        client.disconnect()
    return history.messages[0].message, None
