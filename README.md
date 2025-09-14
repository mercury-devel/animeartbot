# AnimeArt Telegram Bot

![Banner](https://i.imgur.com/QtTJdhn.jpeg)

# 📖 Description
- Sends anime art from danbooru.donmai.us as random posts.
- Supports user-defined tags to filter results (e.g., `large_breasts`, `school_uniform`).
- Checks channel subscription; bot works only for subscribers.
- Sends image batches (media groups) for the selected tag.
- Admin commands available for banning/unbanning users.

# ⚙️ Project Setup Guide

Welcome! Below are instructions to run the project locally (Python) or with Docker.

## Getting Started

### 1. Create and configure a Telegram channel

1. Create a channel in Telegram — it helps promote and gate bot usage.
2. Create a Telegram bot and add it to the channel as an admin (needed for subscription checks).

### 2. Configure environment variables

Create a `.env` file in the project root and set values:

```env
API_TOKEN=your_bot_token
adminlist=123456789,987654321  # Telegram admin IDs, comma-separated
api_id=your_api_id_from_my.telegram.org
api_hash=your_api_hash_from_my.telegram.org
proxy=http://user:pass@host:port  # required format: scheme://user:pass@host:port
channel_id=-100123123123  # Channel ID (usually starts with -100)
channel_link=https://t.me/your_channel_invite_or_username
```

Values are read in `config.py`. The `proxy` is required and must be a single string in the `scheme://user:pass@host:port` format.

## Setup Instructions

1. Install Docker (optional)

   Follow the official guide: https://docs.docker.com/engine/install/

2. Run locally (Windows PowerShell)

```powershell
# 1) Ensure Python 3.11+
python --version

# 2) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4) Create .env as above
# 5) Ensure DB exists: base/userdata.db (already in the repo)
#    If missing, create the folder and an empty DB:
# New-Item -ItemType Directory -Path .\base -Force | Out-Null
# sqlite3 .\base\userdata.db "VACUUM;"   # via SQLite CLI if installed

# 6) Start the bot
python bot.py
```

If you want to initialize tables from scratch, use SQL (example):

```sql
CREATE TABLE IF NOT EXISTS userdata (id INTEGER PRIMARY KEY, tag TEXT, dummy INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS banlist (id INTEGER PRIMARY KEY);
CREATE TABLE IF NOT EXISTS stickers (sticker TEXT);
```

3. Run with Docker

```powershell
# Build and start
docker-compose up -d --build

# View container logs
docker logs aniart

# Stop/start
docker stop aniart
docker start aniart

# Remove container
docker rm aniart
```

On Linux/Mac you can also use the `run.sh` helper (menu with build, start/stop, logs, etc.).

## Notes

- `.env` must be set correctly or the bot will not start.
- To check subscription, the bot needs admin rights in your channel.
- In Docker, SQLite data (`base/`) is stored in the `aniartdb` volume to persist between restarts.
- Do not commit real tokens to public repos. Keep `.env` in `.gitignore` and rotate credentials when needed.

# 🚀 Usage

- `/start` — shows the welcome message and a keyboard with `randompost`.
- `randompost` — sends a batch of arts for your tag (or no tag).
- `/tag` — shows how to set a tag.
- `/seetag` — displays your current tag.
- `!tag your_tag` — set your tag.

Additionally:
- Channel subscription (`channel_id`) is required. If not subscribed, the bot will suggest visiting `channel_link`.
- Admin commands in chat:
  - `ban <telegram_id>` — ban a user
  - `pardon <telegram_id>` — unban a user

## Admin Tools

These helper scripts use the same `.env` and SQLite DB and should not run at the same time as the main bot (to avoid polling conflicts). Stop the bot container/process before using them.

- `add_stickers.py`: DM the bot from your admin account and send any sticker — it will be saved into `base/userdata.db` → `stickers` table.

```powershell
.\.venv\Scripts\Activate.ps1
python add_stickers.py
# In Telegram DM (from admin account):
# /start
# Send stickers → "Added." when saved
# /count → shows how many are saved
```

- `review_stickers.py`: Sends ALL saved stickers to the admin with inline buttons on each message.
   - Delete: removes the sticker from the DB and clears buttons on that message
   - Keep: leaves the sticker and clears buttons on that message

```powershell
.\.venv\Scripts\Activate.ps1
python review_stickers.py
# In Telegram DM (from admin account):
# /review → bot sends all stickers for review with Delete/Keep buttons
```

Notes:
- The admin account is taken from the first ID in `adminlist` inside `.env`.
- The DB path is `base/userdata.db`; the `stickers` table is created automatically if missing.
- Ensure you have DM’d the bot at least once (e.g., /start) so it can message you.
