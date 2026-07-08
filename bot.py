from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import re
from aiohttp import web
import asyncio

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Добавь переменную TOKEN в Render")

# --- Обработчики Telegram бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Введите номер телефона.\n"
        "Поддерживаются все человеческие (российские) форматы:\n"
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
        
        # Если номер начинается с 8, заменяем на +7
        if digits_only.startswith('8'):
            digits_only = '7' + digits_only[1:]
        
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

# --- Эндпоинт для пингования ---
async def health_check(request):
    """Простой эндпоинт для UptimeRobot, возвращает статус 200 OK"""
    return web.Response(text="OK", status=200)

async def start_web_server():
    """Запускает aiohttp веб-сервер для обработки пингов"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    await site.start()
    print("✅ Веб-сервер для пингов запущен на порту 8080")
    return runner

# --- Основная функция ---
def main():
    # Запускаем веб-сервер для пингов
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Создаем приложение бота
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Запускаем веб-сервер в фоне
    loop.create_task(start_web_server())
    
    print("✅ Бот успешно запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
