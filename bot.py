import os
from flask import Flask, request
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

TOKEN = os.environ.get('8697083558:AAEVXEs2kUAUdDOSLPigtOY_xoguZWVwYL8')

if not TOKEN:
    print("❌ Ошибка: Добавь TELEGRAM_TOKEN в Environment Variables!")
    exit(1)

logging.basicConfig(level=logging.INFO)

# Создаем приложение бота
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Привет! Бот работает 24/7 на Render!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Напиши что-нибудь, я отвечу!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'📝 Ты написал: {update.message.text}')

# Добавляем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Вебхук
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return 'ok', 200

@app.route('/')
def index():
    return '🤖 Бот работает!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Бот запущен на порту {port}")
    app.run(host='0.0.0.0', port=port)