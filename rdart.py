from pyrogram.enums import ParseMode
from threading import Thread
import requests
import asyncio
import random
import json
import os
from config import *


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
        try:
            for _ in range(10):
                try:
                    art_data = requests.get(
                        url="https://danbooru.donmai.us/posts/random.json",
                        params=params,
                        proxies=proxies
                    )
                    art = art_data.json()
                    #print(json.dumps(art, indent=4))
                    tags = art["tag_string"].split(" ")
                    art_url = art["large_file_url"]
                    break
                except:
                    pass
            if not art_url:
                return
            file_ext = art["file_ext"]
            post_link = f"\n{self.random_emoji()}<b><u>Ссылка на пост:</u></b> <a href='https://danbooru.donmai.us/posts/{art['id']}'>открыть</a>"
            tag_string = f"{self.random_emoji()}<b><u>Теги:</u></b>\n"
            for tag in tags:
                tag_string += f"<code>{tag}</code> "
            tag_string += "\n"
            #art_name = art_url.split("/")[-1]
            #source = requests.get(url=art_url, proxies=proxies).content
            #art_path = "arts/"+art_name
            #f = open(art_path, "wb")
            #f.write(source)
            #f.close()
            
            caption = tag_string[:974] + "\n" + post_link
            if file_ext in ["jpg", "png", "webp"]:
                self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=art_url,
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )
            elif file_ext in ["mp4", "webm"]:
                self.bot.send_video(
                    chat_id=self.chat_id,
                    video=art_url,
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )
        except:
            pass
