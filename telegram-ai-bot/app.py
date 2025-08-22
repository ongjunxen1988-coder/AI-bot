import os
from fastapi import FastAPI, Request
from telegram import Update, Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_BASE = os.getenv("WEBHOOK_BASE")

if not TOKEN or not WEBHOOK_BASE:
    raise RuntimeError("请设置 TELEGRAM_BOT_TOKEN 和 WEBHOOK_BASE 环境变量")

bot = Bot(TOKEN)
app = FastAPI()

@app.get("/")
async def root():
    return {"ok": True, "message": "Bot is running!"}

@app.post(f"/webhook/{TOKEN}")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)

    if update.message and update.message.text:
        await bot.send_message(
            chat_id=update.message.chat_id,
            text=f"快速回复: {update.message.text}"
        )

    return {"ok": True}
