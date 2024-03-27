from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

TELEGRAM_BOT_TOKEN = '<your token>'
WB_API_URL = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm='

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties())