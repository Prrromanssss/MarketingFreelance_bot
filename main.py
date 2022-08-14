import asyncio
import telebot.async_telebot
import config
import message as msg_text
from telebot import types
import models


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def basic_commands(message):
    models.db_object.db_insert(bot, message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='О нас'))
    markup.add(types.KeyboardButton(text='Услуги'))
    markup.add(types.KeyboardButton(text='Поддержка'))
    text = msg_text.RegularUser().start()
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    await services(message)


@bot.message_handler(commands=['admin'])
async def administration(message):
    ...


@bot.message_handler(content_types=['text'])
async def get_messages(message):
    if message.text == 'О нас':
        text = msg_text.Basement().about()
        await bot.send_message(chat_id=message.chat.id, text=text)
    elif message.text == 'Услуги':
        await services(message)
    elif message.text == 'Поддержка':
        text = msg_text.Basement().support_start()
        await bot.send_message(chat_id=message.chat.id, text=text)
    elif msg_text.dev_bots.flag_develop_bots.get(message.chat.id):
        del msg_text.dev_bots.flag_develop_bots[message.chat.id]
        text = message.text
        await bot.send_message(chat_id=config.ADMINS['sourr_cream'], text=text)  # decotto
        await bot.send_message(chat_id=config.ADMINS['sourr_cream'], text=text)  # qzark
        text = msg_text.dev_bots.finish()
        await bot.send_message(chat_id=message.chat.id, text=text)
    elif msg_text.prom_tg.flag_prom_tg.get(message.chat.id):
        text = f'<strong>{msg_text.prom_tg.category.get(message.chat.id)}</strong>\n{message.text}'
        del msg_text.prom_tg.flag_prom_tg[message.chat.id]
        del msg_text.prom_tg.category[message.chat.id]
        await bot.send_message(chat_id=config.ADMINS['sourr_cream'], text=text)  # qzark
        text = msg_text.prom_tg.finish()
        await bot.send_message(chat_id=message.chat.id, text=text)


async def services(message):
    text = msg_text.Basement().services()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Разработка чат-ботов', callback_data='develop_bots'))
    markup.add(types.InlineKeyboardButton(text='Реклама у блогеров', callback_data='bloggers'))
    markup.add(types.InlineKeyboardButton(text='Продвижение в телеграмм', callback_data='promotion_telegram'))
    markup.add(types.InlineKeyboardButton(text='Создание сайтов', callback_data='sites'))
    markup.add(types.InlineKeyboardButton(text='Дизайн', callback_data='design'))
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'develop_bots')
async def develop_bots(callback):
    text = msg_text.dev_bots.start()
    msg_text.dev_bots.flag_develop_bots[callback.message.chat.id] = True
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'bloggers')
async def bloggers(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'promotion_telegram')
async def prom_telegram(callback):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton(text='Рассылки в Telegram', callback_data='prom_tg_Рассылки в Telegram'))
    markup.add(types.InlineKeyboardButton(text='Парсинг подписчиков', callback_data='prom_tg_Парсинг подписчиков'))
    markup.add(types.InlineKeyboardButton(text='Инвайт в группы', callback_data='prom_tg_Инвайт в группы'))
    markup.add(types.InlineKeyboardButton(text='PR компании', callback_data='prom_tg_PR компании'))
    markup.add(types.InlineKeyboardButton(text='Циклические публикации в чатах',
                                          callback_data='prom_tg_Циклические публикации в чатах'))
    markup.add(types.InlineKeyboardButton(text='Посев нативных комментариев',
                                          callback_data='prom_tg_Посев нативных комментариев'))
    text = msg_text.prom_tg.start()
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'prom_tg' in callback.data)
async def prom_telegram_2(callback):
    text = msg_text.prom_tg.prom_tg_markup()
    msg_text.prom_tg.category[callback.message.chat.id] = callback.data.split('_')[-1]
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'sites')
async def sites(callback):
    text = msg_text.site.start()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Заполнить бриф', callback_data='site_2_Заполнить бриф'))
    markup.add(types.InlineKeyboardButton(text='Нужна помощь специалиста',
                                          callback_data='site_2_Нужна помощь специалиста'))
    await bot.send_message(chat_id=callback.message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'site_2' in callback.data)
async def sites_2(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'design')
async def design(callback):
    ...


async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())
