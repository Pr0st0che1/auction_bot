from telegram import Bot

from django.conf import settings

# Создаем экземпляр бота с токеном из settings.py
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

def send_auction_end_notification(user_id, lot_name, final_price):
    message = f"🏆 Аукцион завершён!\n\nЛот: {lot_name}\nФинальная цена: {final_price} 💰"
    try:
        bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")
