# -*- coding: utf-8 -*-
"""
В этом модуле представлена отправка новостей
роллер спорта через telegram-бот
"""
import asyncio
import os
import telegram
from parse_rollerme import RollermeParser
from parse_frs import FRSParser, FRS_EVENTS_URL

TOKEN = os.getenv('TG_ROLLER')
CHAT_ENV_VARS = (
    'TG_MY_CHAT_ID_ROLLER',
    'TG_RAF_CHAT_ID_ROLLER',
)

messages = list()


def chat_ids():
    return (os.getenv(env_var) for env_var in CHAT_ENV_VARS)


def roller_me_announces():
    roller_me = RollermeParser()
    announces = roller_me.get_fresh_announces()
    if announces:
        for title in announces:
            description, card, announce_url = announces[title]
            # пример сообщения с html-разметкой
            # messages.append(
            #     f'<b>{title}</b>\n\n{description}\n\n<a href="{announce_url}"'
            #     f'>Подробнее</a>')
            messages.append(
                f'*Новости Roller Me*\n\n*{title}*\n\n{description}\n\n'
                f'[Подробнее]({announce_url})'
            )


def frs_announces():
    frs = FRSParser()
    current_month_events = frs.get_current_month_events()
    future_month_events = frs.get_future_month_events()
    for events in (current_month_events, future_month_events):
        if events:
            messages.append(
                f'*Новости ФРС*\n\n{events}\n\n[Подробнее]({FRS_EVENTS_URL}'
            )


roller_me_announces()
frs_announces()

# пример отправки сообщения через requests
# import requests
# for message in messages:
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?" \
#           f"chat_id={CHAT_ID}&text={message}"
#     requests.get(url).json()


async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        for chat_id in chat_ids():
            for message in messages:
                # пример отправки сообщения с html-разметкой
                # await bot.sendMessage(text=message, chat_id=CHAT_ID, parse_mode='html')
                await bot.sendMessage(
                    text=message, chat_id=chat_id,
                    parse_mode='markdown', disable_web_page_preview=True)

if __name__ == '__main__':
    asyncio.run(main())
