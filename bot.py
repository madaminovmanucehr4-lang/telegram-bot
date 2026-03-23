import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


app = Flask(__name__)


TOKEN = os.environ.get('8697083558:AAEVXEs2kUAUdDOSLPigtOY_xoguZWVwYL8')

if not TOKEN:
    print("❌ Ошибка: Добавь TELEGRAM_TOKEN в Environment Variables!")
    exit(1)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Создаем приложение бота
bot_app = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Привет! Я бот работаю 24/7 на бесплатном хостинге!')

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Просто напиши мне что-нибудь, я отвечу!')

# Обработчик сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f'📝 Ты написал: {user_message}')

# Регистрируем команды
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("help", help_command))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Вебхук для Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    """Получаем обновления от Telegram"""
    update = Update.de_json(request.get_json(), bot_app.bot)
    bot_app.process_update(update)
    return 'ok', 200

# Проверка что бот жив
@app.route('/')
def index():
    return '🤖 Бот работает!', 200

if __name__ == '__main__':
    # Запускаем сервер
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Бот запущен на порту {port}")
    app.run(host='0.0.0.0', port=port)