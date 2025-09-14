from aiogram import Bot, Dispatcher, types, executor
from config import API_TOKEN, adminlist
import sqlite3
from typing import Optional

ADMIN_ID = int(adminlist[0]) if adminlist else None
DB_PATH = 'base/userdata.db'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def ensure_table() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS stickers (sticker TEXT)")
        conn.commit()
    finally:
        conn.close()


def sticker_exists(file_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM stickers WHERE sticker = ? LIMIT 1", (file_id,))
        return cur.fetchone() is not None
    finally:
        conn.close()


def add_sticker(file_id: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO stickers(sticker) VALUES (?)", (file_id,))
        conn.commit()
    finally:
        conn.close()


def stickers_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM stickers")
        (cnt,) = cur.fetchone() or (0,)
        return int(cnt)
    finally:
        conn.close()


@dp.message_handler(commands=["start", "help"]) 
async def cmd_start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Hello! This tool is for admins only.")
        return
    ensure_table()
    await message.answer(
        "Send me any sticker to add it to the database.\n"
        "Commands:\n"
        "/count — show how many stickers are saved"
    )


@dp.message_handler(commands=["count"]) 
async def cmd_count(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Admins only")
        return
    ensure_table()
    await message.answer(f"Stickers saved: {stickers_count()}")


@dp.message_handler(content_types=[types.ContentType.STICKER])
async def on_sticker(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        # Ignore non-admin stickers silently to avoid spam
        return
    ensure_table()
    file_id: Optional[str] = message.sticker.file_id if message.sticker else None
    if not file_id:
        await message.answer("Could not read sticker file_id.")
        return
    if sticker_exists(file_id):
        await message.answer("Already exists.")
        return
    try:
        add_sticker(file_id)
        await message.answer("Added.")
    except Exception as e:
        await message.answer(f"Failed to add: {e}")


if __name__ == "__main__":
    ensure_table()
    executor.start_polling(dp)
