from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_hi = KeyboardButton('Привет! 👋')
button_back = KeyboardButton('🔙​Назад')
button_cryptovalue = KeyboardButton('👨‍💻 ​Курсы криптовалют')
button_botinfo = KeyboardButton('🖥️ Информация о боте')
button_fiatvalue = KeyboardButton('💱​ ​Курсы фиатных валют')
button_USD = KeyboardButton('💵 Доллар')
button_EUR = KeyboardButton('💶 Евро')
button_CNY = KeyboardButton('💴 Юань')
button_subscribe = KeyboardButton('🔔 Подписаться')
button_unsubscribe = KeyboardButton('🔕 Отписаться')
button_yessub = KeyboardButton('✅ Да')
button_yesunsub = KeyboardButton('❎​ Да')
button_debug_digest = KeyboardButton('👀​ Preview Digest')
button_view_subs = KeyboardButton('🧑 View Subscribers')
button_reload_data = KeyboardButton('🪠​ Force Reload Data')

botinfo = 'Этот бот создан на Python с использованием aiogram.\n\nИнформация о фиатных валютах парсится с https://www.cbr-xml-daily.ru/daily_json.js\n\nИнформация о криптовалютах парсится с https://www.cryptocompare.com/'
surewantsub = "*Подписка на актуальные котировки:*\n\nКаждый день в *16:00* по Москве вам будет приходить рассылка с актуальными котировками мировых валют и криптовалют.\n\n*Вы хотите подписаться?*"
surewantunsub = "Отписка от котировок *лишает вас*\nежедневной актуальной информации.\n\n*Вы хотите отписаться?*"
startmessage = "👋 *Привет!*\n\nЯ могу предоставлять актуальные курсы _криптовалют_ и _мировых валют!_"
menumessage = "✅ *​Выберите действие, чтобы продолжить:*"
pickvalute = "❓ ​Выберите валюту:"
sucessfullysub = "*Вы успешно подписались на рассылку!*"
sucessfullyunsub = "*Вы успешно отписались от рассылки!*"
notasub = "*Вы и так не подписаны на рассылку.*"
backtomenu = "*Вы вернулись в главное меню.*"
adminmessage = "🔧 *Вы вошли в меню администратора*"
notadmin = "🚫 *У вас нет прав администратора*"

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)
menu_subscriber_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cryptovalue, button_fiatvalue, button_botinfo, button_unsubscribe)
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cryptovalue, button_fiatvalue, button_botinfo, button_subscribe)
fiat_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button_USD, button_EUR, button_CNY
    ).add(button_back)
back = ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)
sub_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_yessub,button_back)
unsub_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_yesunsub, button_back)
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_debug_digest, button_view_subs, button_reload_data, button_back)