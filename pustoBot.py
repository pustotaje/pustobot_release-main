import logging
import importlib
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

from datetime import datetime, timedelta
import pustoEssentials
import pustoFiat
import pustoCrypto
import argparse

parser = argparse.ArgumentParser(description='Bot configuration')
parser.add_argument('--mh', type=int, default=13, help='Час отправки рассылки')
parser.add_argument('--mmin', type=int, default=30, help='Минута отправки рассылки')
parser.add_argument('--rh', type=int, default=12, help='Час обновления данных')
parser.add_argument('--rmin', type=int, default=30, help='Минута обновления данных')
args = parser.parse_args()

admin_users = [783735329, 777920257]
API_TOKEN = '6405101803:AAHj4PegYpa7qnFaimskg-o5oj8fuWX8FO4'

lasttimestamp = None

MessageSendHour = args.mh
MessageSendMinute = args.mmin

DataReloadHour = args.rh
DataReloadMinute = args.rmin

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

subscribed_users = set()

#кнопки взаимодействия с ботом
button_hi = pustoEssentials.button_hi
button_back = pustoEssentials.button_back
button_cryptovalue = pustoEssentials.button_cryptovalue
button_botinfo = pustoEssentials.button_botinfo
button_fiatvalue = pustoEssentials.button_fiatvalue
button_USD = pustoEssentials.button_USD
button_EUR = pustoEssentials.button_EUR
button_CNY = pustoEssentials.button_CNY
button_subscribe = pustoEssentials.button_subscribe
button_unsubscribe = pustoEssentials.button_unsubscribe
button_yessub = pustoEssentials.button_yessub
button_yesunsub = pustoEssentials.button_yesunsub

#разметки клавиатур
greet_kb = pustoEssentials.greet_kb
menu_subscriber_kb = pustoEssentials.menu_subscriber_kb
menu_kb = pustoEssentials.menu_kb
fiat_kb = pustoEssentials.fiat_kb
back = pustoEssentials.back
sub_kb = pustoEssentials.sub_kb
unsub_kb = pustoEssentials.unsub_kb
admin_kb = pustoEssentials.admin_kb

#ответы бота
startmessage = pustoEssentials.startmessage
menumessage = pustoEssentials.menumessage
pickvalute = pustoEssentials.pickvalute
sucessfullysub = pustoEssentials.sucessfullysub
sucessfullyunsub = pustoEssentials.sucessfullyunsub
backtomenu = pustoEssentials.backtomenu
botinfo = pustoEssentials.botinfo
surewantsub = pustoEssentials.surewantsub
notasub = pustoEssentials.notasub
adminmessage = pustoEssentials.adminmessage
surewantunsub = pustoEssentials.surewantunsub
notadmin = pustoEssentials.notadmin

async def main():
    await asyncio.gather(
        scheduler(),
        send_message_to_subscribers(),
        reload_gather_data()
    )

async def reload_gather_data():
    global lasttimestamp
    importlib.reload(pustoFiat)
    importlib.reload(pustoCrypto)
    lasttimestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print(f"Последнее обновление данных: {lasttimestamp}")
    
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(startmessage, reply_markup=greet_kb, parse_mode="Markdown")

@dp.message_handler(commands=['admin'])
async def enter_admin_menu(message: types.Message):
    if message.from_user.id in admin_users:
        await message.reply(adminmessage, reply_markup=admin_kb, parse_mode="Markdown")
    elif message.from_user.id in subscribed_users:
        await message.reply(notadmin, reply_markup=menu_subscriber_kb, parse_mode="Markdown")
    else:
        await message.reply(notadmin, reply_markup=menu_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == '👀​ Preview Digest')
async def preview_digest(message: types.Message):
    if message.from_user.id in admin_users:
            await message.reply(f"*Ваш ежедневный дайджест:*\n\nПо состоянию на {lasttimestamp}:\n\n_Курсы криптовалют_:\n\n{pustoCrypto.genout('BTC')}\n{pustoCrypto.genout('ETH')}\n{pustoCrypto.genout('BNB')}\n{pustoCrypto.genout('LTC')}\n\n{pustoCrypto.genout('TONCOIN')}\n{pustoCrypto.genout('MATIC')}\n{pustoCrypto.genout('TRX')}\n{pustoCrypto.genout('XRP')}\n\n{pustoCrypto.genout('DOGE')}\n{pustoCrypto.genout('SHIB')}\n\n_Курсы мировых валют_:\n\n{pustoFiat.outputUSDdigest}\n{pustoFiat.outputEURdigest}\n{pustoFiat.outputCNYdigest}\n", parse_mode='Markdown', reply_markup=admin_kb)
    elif message.from_user.id in subscribed_users:
        await message.reply(notadmin, reply_markup=menu_subscriber_kb, parse_mode="Markdown")
    else:
        await message.reply(notadmin, reply_markup=menu_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == '🪠​ Force Reload Data')
async def force_reload_data(message: types.Message):
    if message.from_user.id in admin_users:
        updating_message = await message.reply("🔃​ *Обновляю курсы валют...*", reply_markup=admin_kb, parse_mode="Markdown")
        await reload_gather_data()
        await bot.delete_message(chat_id=updating_message.chat.id, message_id=updating_message.message_id)
        await message.reply("✅ *Курсы валют успешно обновлены.*", reply_markup=admin_kb, parse_mode="Markdown")
    elif message.from_user.id in subscribed_users:
        await message.reply(notadmin, reply_markup=menu_subscriber_kb, parse_mode="Markdown")
    else:
        await message.reply(notadmin, reply_markup=menu_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == '🧑 View Subscribers')
async def view_subsdribers(message: types.Message):
    if message.from_user.id in admin_users:
            await message.reply(f"Subscribers:\n{subscribed_users}", reply_markup=admin_kb, parse_mode="Markdown")
    elif message.from_user.id in subscribed_users:
        await message.reply(notadmin, reply_markup=menu_subscriber_kb, parse_mode="Markdown")
    else:
        await message.reply(notadmin, reply_markup=menu_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == 'Привет! 👋')
async def send_menu(message: types.Message):
        await message.reply(menumessage, reply_markup=menu_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == '👨‍💻 ​Курсы криптовалют')
async def send_crypto(message: types.Message):
    await message.reply(f"💎 По состоянию на {lasttimestamp}:\n{pustoCrypto.genout('BTC')}\n{pustoCrypto.genout('ETH')}\n{pustoCrypto.genout('BNB')}\n{pustoCrypto.genout('LTC')}\n\n{pustoCrypto.genout('TONCOIN')}\n{pustoCrypto.genout('MATIC')}\n{pustoCrypto.genout('TRX')}\n{pustoCrypto.genout('XRP')}\n\n{pustoCrypto.genout('DOGE')}\n{pustoCrypto.genout('SHIB')}", reply_markup=back)

@dp.message_handler(lambda message: message.text == '💱​ ​Курсы фиатных валют')
async def send_fiat(message: types.Message):
    await message.reply(pickvalute, reply_markup=fiat_kb)

@dp.message_handler(lambda message: message.text == '💵 Доллар')
async def send_usd(message: types.Message):
    await message.reply(f"💵 По состоянию на {lasttimestamp}:\n1 $ = {pustoFiat.CurUSDValue} {pustoFiat.diffUSD} ({pustoFiat.PercentUSD})\n", reply_markup=fiat_kb)

@dp.message_handler(lambda message: message.text == '💶 Евро')
async def send_eur(message: types.Message):
    await message.reply(f"💶 По состоянию на {lasttimestamp}:\n1 € = {pustoFiat.CurEURValue} {pustoFiat.diffEUR} ({pustoFiat.PercentEUR})\n", reply_markup=fiat_kb)

@dp.message_handler(lambda message: message.text == '💴 Юань')
async def send_cny(message: types.Message):
    await message.reply(f"💴 По состоянию на {lasttimestamp}:\n1 ¥ = {pustoFiat.CurCNYValue} {pustoFiat.diffCNY} ({pustoFiat.PercentCNY})\n", reply_markup=fiat_kb)

@dp.message_handler(lambda message: message.text == '🔔 Подписаться')
async def subscribesure(message: types.Message):
    await message.reply(surewantsub, reply_markup=sub_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == '✅ Да')
async def subscribe(message: types.Message):
    global subscribed_users
    subscribed_users.add(message.from_user.id)
    await message.reply(sucessfullysub, reply_markup=menu_subscriber_kb, parse_mode='Markdown')

@dp.message_handler(lambda message: message.text == '🔕 Отписаться')
async def unsubscribe(message: types.Message):
    await message.reply(surewantunsub, reply_markup=unsub_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == '❎​ Да')
async def unsubscribe(message: types.Message):
    global subscribed_users
    if message.from_user.id in subscribed_users:
        subscribed_users.remove(message.from_user.id)
        await message.reply(sucessfullyunsub, reply_markup=menu_kb, parse_mode='Markdown')
    else:
        await message.reply(notasub, reply_markup=menu_kb, parse_mode='Markdown')

@dp.message_handler(lambda message: message.text == '🔙​Назад')
async def goback(message: types.Message):
    if message.from_user.id in subscribed_users:
        await message.reply(backtomenu, reply_markup=menu_subscriber_kb, parse_mode="Markdown")
    else:
        await message.reply(backtomenu, reply_markup=menu_kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == '🖥️ Информация о боте')
async def send_info(message: types.Message):
    await message.reply(f"Последнее обновление данных: {lasttimestamp}\n\n{botinfo}", reply_markup=back)

@dp.message_handler(lambda message: message.text == 'Debug Digest')
async def send_info(message: types.Message):
    await message.reply(f"*Ваш ежедневный дайджест:*\n\nПо состоянию на {lasttimestamp}:\n\n_Курсы криптовалют_:\n\n{pustoCrypto.genout('BTC')}\n{pustoCrypto.genout('ETH')}\n{pustoCrypto.genout('BNB')}\n{pustoCrypto.genout('LTC')}\n\n{pustoCrypto.genout('TONCOIN')}\n{pustoCrypto.genout('MATIC')}\n{pustoCrypto.genout('TRX')}\n{pustoCrypto.genout('XRP')}\n\n{pustoCrypto.genout('DOGE')}\n{pustoCrypto.genout('SHIB')}\n\n_Курсы мировых валют_:\n\n{pustoFiat.outputUSDdigest}\n{pustoFiat.outputEURdigest}\n{pustoFiat.outputCNYdigest}\n", parse_mode='Markdown', reply_markup=back)

async def send_message_to_subscribers():
    global subscribed_users
    for user_id in subscribed_users:
        await bot.send_message(user_id, f"*Ваш ежедневный дайджест:*\n\nПо состоянию на {lasttimestamp}:\n\n_Курсы криптовалют_:\n\n{pustoCrypto.genout('BTC')}\n{pustoCrypto.genout('ETH')}\n{pustoCrypto.genout('BNB')}\n{pustoCrypto.genout('LTC')}\n\n{pustoCrypto.genout('TONCOIN')}\n{pustoCrypto.genout('MATIC')}\n{pustoCrypto.genout('TRX')}\n{pustoCrypto.genout('XRP')}\n\n{pustoCrypto.genout('DOGE')}\n{pustoCrypto.genout('SHIB')}\n\n_Курсы мировых валют_:\n\n{pustoFiat.outputUSDdigest}\n{pustoFiat.outputEURdigest}\n{pustoFiat.outputCNYdigest}\n", parse_mode='Markdown')

async def scheduler():
    while True:
        now = datetime.now()
        next_message_trigger = now.replace(hour=MessageSendHour, minute=MessageSendMinute, second=0, microsecond=0)
        next_reload_trigger = now.replace(hour=DataReloadHour, minute=DataReloadMinute, second=0, microsecond=0)
        
        if now > next_message_trigger:
            next_message_trigger += timedelta(days=1)
        if now > next_reload_trigger:
            next_reload_trigger += timedelta(days=1)
        
        time_left_message = next_message_trigger - now
        time_left_reloading = next_reload_trigger - now
        logging.info(f"Отправка рассылки через: {time_left_message}")
        logging.info(f"Обновление данных о курсах через:{time_left_reloading}")
        logging.info(f"Подписчиков: {len(subscribed_users)}: {subscribed_users}")
        logging.info(f"{lasttimestamp}\n\n")
        
        if now.hour == DataReloadHour and now.minute == DataReloadMinute:
            await reload_gather_data()
            next_reload_trigger += timedelta(days=1)
            await asyncio.sleep(70) 

        if now.hour == MessageSendHour and now.minute == MessageSendMinute:
            await send_message_to_subscribers()
            next_message_trigger += timedelta(days=1)
            await asyncio.sleep(70)
        
        await asyncio.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)