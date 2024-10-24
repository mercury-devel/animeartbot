from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from sqlite_requests import Sqlite
from pyrogram import Client
from rdart import RandomArt
import random
from config import *


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

scheme, rest = proxy.split("://")
credentials, host_port = rest.split("@")
username, password = credentials.split(":")
hostname, port = host_port.split(":")

proxy_dict = {
    "scheme": scheme,
    "hostname": hostname,
    "port": int(port),
    "username": username,
    "password": password
}
pyro = Client(
    "alice",
    api_id=api_id, api_hash=api_hash,
    bot_token=API_TOKEN,
    proxy=proxy_dict
)
pyro.start()

start_msg = '''
🌸Привет! Этот бот отправляет арты с danbooru.donmai.us
⚡️Нажми на кнопку "randompost" чтобы увидеть новое фото
Другие команды:
🚀/start - Запустить бота
🖼/randompost - отправка поста
🔎/tag - настройка тегов
👁/seetag - посмотреть свой тег
'''
sql_rq = Sqlite()
stickers = [sticker[0] for sticker in sql_rq.select("select sticker from stickers")]


@dp.message_handler(content_types=[types.ContentType.ANY])
async def echo(message: types.Message):
    sticker = random.choice(stickers)
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_status = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    user_status = user_status.status
    '''
    if message.sticker:
        sticker = message.sticker.file_id
        sql_rq.insert_delete(f"insert into stickers values ('{sticker}')")
        print(message.sticker.file_id)'''
    user_banned = sql_rq.select(f"select id from banlist where id = {user_id}")
    user_exists = sql_rq.select(f"select id from userdata where id = {user_id}")
    if not user_exists:
        sql_rq.insert_delete(f"insert into userdata values ({user_id},'', 0)")
    txt = message.text
    if txt is not None and not user_banned:
        if user_status in ["member", "creator", "administrator"] and not user_banned:
            if user_id in adminlist:
                if txt.find("ban") > -1:
                    banned_id = txt.split(" ")[1]
                    sql_rq.insert_delete(f"insert into banlist values ({banned_id})")
                    await bot.send_message(
                        chat_id,
                        f'⛔️<code>{banned_id}</code> banned!',
                        parse_mode="html"
                    )
                if txt.find("pardon") > -1:
                    banned_id = txt.split(" ")[1]
                    sql_rq.insert_delete(f"delete from banlist where id = ({banned_id})")
                    await bot.send_message(
                        chat_id,
                        f'✅<code>{banned_id}</code> unbanned!',
                        parse_mode="html"
                    )

            if txt.find("/start") > -1:
                await bot.send_sticker(
                    chat_id=chat_id,
                    sticker=sticker
                )
                if chat_id < 0:
                    keyboard = types.ReplyKeyboardRemove()
                else:
                    kb = [[types.KeyboardButton(text="randompost")]]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await bot.send_message(
                    chat_id,
                    start_msg,
                    reply_markup=keyboard
                )

            if txt.find("randompost") > -1:
                tag = sql_rq.select(f"select tag from userdata where id = {user_id}")[0][0]
                rdart = RandomArt(
                    tag=tag,
                    chat_id=chat_id,
                    bot=pyro
                )
                rdart.start()
            if txt.find("/tag") > -1:
                await bot.send_message(
                    chat_id,
                    '🔎Для ввода тега пишите !tag (ваш тег). Например: <code>!tag large_breasts</code>',
                    parse_mode="html"
                )
            if txt.find("/seetag") > -1:
                tag = sql_rq.select(f"select tag from userdata where id = {user_id}")[0][0]
                if tag:
                    await bot.send_message(
                        chat_id,
                        f'🍎Твой тег: {tag}'
                    )
                else:
                    await bot.send_message(
                        chat_id,
                        '🍏У тебя нету тегов'
                    )
            if txt.find("!tag") > -1:
                tag_string = txt[5:]
                sql_rq.insert_delete(f"update userdata set tag = '{tag_string}' where id = {user_id}")
                await bot.send_message(
                    chat_id,
                    f'🍊Тег {tag_string} удачно установлен!'
                )
        else:
            if chat_id > 0:
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton("🔗Ссылка на канал", url=channel_link))
                await bot.send_message(
                    chat_id=chat_id,
                    text="Чтоб пользоваться ботом подпишись на канал\nПосле подписки бот заработает",
                    reply_markup=keyboard
                )



executor.start_polling(dp, skip_updates=True)
