from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")  # Токен из переменных окружения

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаём кнопку для отправки номера
    button = KeyboardButton("📱 Отправить номер", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    
    await update.message.reply_text(
        "Нажми кнопку, чтобы поделиться номером телефона:",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number
    
    # Убираем все лишние символы, оставляем только цифры
    clean_phone = ''.join(filter(str.isdigit, phone))
    
    # Формируем ссылку
    result = f"t.me/{clean_phone}"
    
    await update.message.reply_text(
        f"✅ Ваш номер: {phone}\n"
        f"🔗 Ссылка: {result}"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
