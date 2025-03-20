import os
from django.conf import settings
from dotenv import load_dotenv
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Загружаем переменные окружения из файла .env
load_dotenv()

# Устанавливаем переменную окружения для Django (перед импортом настроек Django)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_bot.settings')

# Импортируем и используем settings после установки переменной окружения
from django.conf import settings

# Подставляем токен бота напрямую
TOKEN = '7501517411:AAEzw9fOxnTsI5qxuxRuGbX9tYgvBQDd9uE'

# Создаем приложение с заданием тайм-аута
application = Application.builder().token(TOKEN).build()

# Устанавливаем тайм-аут для HTTP-запросов
application.bot.set_http_timeout(30)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔎 Найти лоты", callback_data='find_lots')],
        [InlineKeyboardButton("📜 Мои ставки", callback_data='my_bids')],
        [InlineKeyboardButton("⚙️ Настройки", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Добро пожаловать в аукцион!\nВыберите действие:",
        reply_markup=reply_markup
    )


# Функция для обработки кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'find_lots':
        await query.message.reply_text("🔎 Выберите категорию лотов:")
        # Здесь можно добавить код для вывода категорий
    elif query.data == 'my_bids':
        await query.message.reply_text("📜 Ваши активные ставки:")
        # Здесь можно добавить код для показа ставок
    elif query.data == 'settings':
        await query.message.reply_text("⚙️ Настройки профиля:")
        # Здесь можно добавить код для изменения настроек


# Основная функция для запуска бота
def main():
    # Создаем приложение бота
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд и кнопок
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Бот запущен...")
    # Запуск бота с использованием long polling
    app.run_polling()


if __name__ == "__main__":
    main()
