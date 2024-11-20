from pyrogram.enums import ParseMode
from threading import Thread
import requests
import asyncio
import random
from config import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import time

class RandomArt(Thread):
    def __init__(self, tag, chat_id, bot):
        Thread.__init__(self)
        self.tag = tag
        self.chat_id = chat_id
        self.bot = bot
        self.emojies = "🍏🍎🍐🍋🍊🍓🫐🍒🍍🍅🍔🍟🍕🍺🍻🍫🍷🌙🌞🌼🌸🌺🌍🌟✨⚡️💥🔥☀️🍥❤️🧡💛💚💙💜"

    def random_emoji(self):
        em = ""
        while not em:
            em = random.choice(self.emojies)
        return em

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        proxies = {
            "http": proxy,
            "https": proxy
        }
        params = {
            "tags": self.tag
        }
        
        # Список для хранения URL изображений и ID постов
        images = []
        
        # Собираем до 10 уникальных изображений
        while len(images) < 10:
            try:
                art_data = requests.get(
                    url="https://danbooru.donmai.us/posts/random.json",
                    params=params,
                )
                #proxies=proxies
                art = art_data.json()
                art_url = art.get("large_file_url")
                file_ext = art.get("file_ext")
                
                if art_url and file_ext in ["jpg", "png"]:
                    images.append(art_url)
                
            except:
                pass
            
            time.sleep(1)

        # Если не нашли подходящих изображений
        if not images:
            return

        # Создаём медиагруппу из собранных изображений
        msg = self.bot.send_message(
            chat_id=self.chat_id,
            text=f"{self.random_emoji()} Результаты по тегу <code>{self.tag}</code>"
        )
        media_group = []
        for art_url in images:
            media_group.append(InputMediaPhoto(media=art_url, parse_mode=ParseMode.HTML))
        
        # Отправляем медиагруппу в чат
        self.bot.send_media_group(
            chat_id=self.chat_id,
            media=media_group,
            reply_to_message_id=msg.id
        )
