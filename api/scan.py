from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import time
import asyncio
import random
from background_task import background
from api.models import Result, Setting, Account
from telethon.tl.types import MessageEntityTextUrl
from django.core.files.base import File


@background()
def get_info(number: str):
    setting = Setting.objects.get(id=1)
    account = random.choice(list(Account.objects.filter(status=True)))
    print('start')
    print(account.name)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(
        "session_create/" + str(account.name),
        setting.api_id,
        setting.api_hash,
        loop=loop
    )
    client.start()
    bot = client.get_entity(setting.bot_link)
    try:
        client.send_message(bot, number)
    except Exception as e:
        print(e)
        client.disconnect()
        return
    time.sleep(0.5)
    counter = 0
    while True:
        if counter == 20:
            client.disconnect()
            return
        history = client(GetHistoryRequest(
            peer=bot,
            offset_id=0,
            offset_date=None, add_offset=0,
            limit=2, max_id=0, min_id=0,
            hash=0))
        if "Расширенный поиск" in history.messages[0].message:
            break

        elif 'Оператор и регион не установлены!' in history.messages[0].message:
            client.disconnect()
            return
        else:
            counter += 1
            time.sleep(0.5)

    text = str(history.messages[0].message)
    for link, inner_text in history.messages[0].get_entities_text(MessageEntityTextUrl):
        text = text.replace(str(inner_text), str(inner_text) + " (" + str(link.url) + ")")
    text = text.replace("ℹ️ Если информация не найдена, закажите «Расширенный поиск»", "")
    path = str(client.download_media(history.messages[1].media, "tg_media/photo"))
    try:
        f = open(path, 'rb')
        file = File(f)
        result = Result.objects.create(number=number, text=text, file=file)
    except FileNotFoundError:
        result = Result.objects.create(number=number, text=text)
    client.disconnect()
    delete_info(result.id)
    return


@background(schedule=60*60*24)
def delete_info(result_id: int):
    result_objects = Result.objects.get(id=result_id)
    result_objects.delete()
    return
