import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 环境变量
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_BASE = os.getenv("WEBHOOK_BASE", "").rstrip("/")

# FastAPI 应用
app = FastAPI()

# Telegram 应用（PTB v22）
application: Application = Application.builder().token(TOKEN).build()

# 处理器
async def start_cmd(update, context):
    await update.message.reply_text("Hi! Bot is alive ✅")

async def echo(update, context):
    msg = update.message.text if update.message else ""
    if msg:
        await update.message.reply_text(f"你说：{msg}")

application.add_handler(CommandHandler("start", start_cmd))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

# 生命周期
@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.start()
    # 自动设置 webhook（可选，但最省心）
    if WEBHOOK_BASE:
        await application.bot.set_webhook(f"{WEBHOOK_BASE}/webhook")

@app.on_event("shutdown")
async def on_shutdown():
    await application.stop()
    await application.shutdown()

# 健康检查
@app.get("/")
async def health():
    return {"status": "ok"}

# Telegram Webhook 接收口（务必返回 200）
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return JSONResponse({"ok": True})
