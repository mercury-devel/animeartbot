from pyrogram.enums import ParseMode
from threading import Thread
import requests
import asyncio
import random
from config import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
        art_url = None
        for _ in range(10):
            try:
                art_data = requests.get(
                    url="https://danbooru.donmai.us/posts/random.json",
                    params=params,
                    proxies=proxies
                )
                art = art_data.json()
                tags = art["tag_string"].split(" ")
                art_url = art["large_file_url"]
                file_ext = art["file_ext"]
                if file_ext in ["jpg", "png", "webp"]:
                    break
            except:
                pass
            time.sleep(1)
        if not art_url:
            return
        tag_string = f"{self.random_emoji()}<b><u>Теги:</u></b>\n"
        for tag in tags:
            tag_string += f"{tag} "
        tag_string += "\n"
        
        button = InlineKeyboardButton(f"{self.random_emoji()} Ссылка на пост:", url=f"https://danbooru.donmai.us/posts/{art['id']}")
        keyboard = InlineKeyboardMarkup([[button]])
        
        msg = self.bot.send_message(
            chat_id=self.chat_id,
            text=tag_string[:4000],
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
        msg_id = msg.id
        self.bot.send_photo(
            chat_id=self.chat_id,
            photo=art_url,
            reply_to_message_id=msg_id
        )

