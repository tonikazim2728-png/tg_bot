from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import re

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Добавь переменную TOKEN в Render")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Введите номер телефона в формате:\n"
        "Например: +79037866914\n\n"
        "Я добавлю t.me/ и покажу ссылку."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # Проверяем, что номер начинается с + и содержит только цифры и +
    if not re.match(r'^\+\d+$', text):
        await update.message.reply_text(
            "❌ Неверный формат!\n"
            "Введите номер с плюсом, например:\n"
            "+79037866914"
        )
        return
    
    # Формируем ссылку
    result = f"t.me/{text}"
    
    await update.message.reply_text(
        f"✅ Ваш номер: {text}\n"
        f"🔗 Ссылка: {result}"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ Бот успешно запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
