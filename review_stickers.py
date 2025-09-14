from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_TOKEN, adminlist
import sqlite3
from typing import List, Tuple
import asyncio

ADMIN_ID = int(adminlist[0]) if adminlist else None
DB_PATH = 'base/userdata.db'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def load_stickers() -> List[Tuple[int, str]]:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS stickers (sticker TEXT)")
        cur.execute("SELECT rowid, sticker FROM stickers")
        rows = cur.fetchall()
        return [(int(r[0]), r[1]) for r in rows if r and r[1]]
    finally:
        conn.close()


def delete_sticker_by_rowid(row_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM stickers WHERE rowid = ?", (row_id,))
        conn.commit()
    finally:
        conn.close()


def kb_controls_row(row_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🗑 Delete", callback_data=f"d:{row_id}"),
        InlineKeyboardButton("✅ Keep", callback_data=f"k:{row_id}")
    )
    return kb


async def send_all_stickers(message: types.Message) -> None:
    if message.from_user.id != ADMIN_ID:
        await message.answer("Admins only")
        return

    rows = load_stickers()
    if not rows:
        await message.answer("No stickers found to review.")
        return

    await message.answer(f"Found {len(rows)} stickers. Sending all for review...")

    for idx, (row_id, file_id) in enumerate(rows, start=1):
        try:
            await message.answer_sticker(file_id, reply_markup=kb_controls_row(row_id))
            # Gentle pacing to avoid flood limits
            await asyncio.sleep(0.05)
        except Exception as e:
            await message.answer(f"Failed to send sticker #{idx}: {e}")


@dp.message_handler(commands=["start"]) 
async def on_start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Hello! This maintenance tool is for admins only.")
        return
    await message.answer("Sticker review ready. Send /review to begin.")


@dp.message_handler(commands=["review"]) 
async def on_review(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Admins only")
        return
    await send_all_stickers(message)


@dp.callback_query_handler(lambda c: c.data and (c.data.startswith("d:") or c.data.startswith("k:")))
async def callbacks(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        await call.answer("Admins only", show_alert=True)
        return

    data = call.data
    action, rowid_str = data.split(":", 1)
    try:
        row_id = int(rowid_str)
    except ValueError:
        await call.answer("Invalid action", show_alert=True)
        return

    if action == "d":
        try:
            delete_sticker_by_rowid(row_id)
            await call.message.edit_reply_markup()
            await call.answer("Deleted")
        except Exception as e:
            await call.answer(f"Delete failed: {e}", show_alert=True)
    elif action == "k":
        try:
            await call.message.edit_reply_markup()
            await call.answer("Kept")
        except Exception:
            await call.answer("Kept")



if __name__ == "__main__":
    executor.start_polling(dp)
