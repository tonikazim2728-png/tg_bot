from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import re

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Добавь переменную TOKEN в Render")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Введите номер телефона.\n"
        "Можно с плюсом или без:\n"
        "+79037866914 или 79037866914\n\n"
        "Я сам добавлю + если нужно."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # Убираем все пробелы и лишние символы, оставляем только цифры и +
    cleaned = re.sub(r'[^\d+]', '', text)
    
    # Если номер начинается с +, оставляем как есть
    if cleaned.startswith('+'):
        phone = cleaned
    else:
        # Если нет +, убираем все лишние символы и добавляем +
        digits_only = re.sub(r'\D', '', cleaned)  # оставляем только цифры
        if not digits_only:
            await update.message.reply_text(
                "❌ Ошибка! Введи номер, например:\n"
                "+79037866914 или 79037866914"
            )
            return
        phone = f"+{digits_only}"
    
    # Формируем ссылку
    result = f"t.me/{phone}"
    
    # Создаём кнопку
    button = InlineKeyboardButton(
        text="🔗 Открыть в Telegram", 
        url=result
    )
    reply_markup = InlineKeyboardMarkup([[button]])
    
    await update.message.reply_text(
        text=f"✅ Номер: {phone}",
        reply_markup=reply_markup
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ Бот успешно запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
