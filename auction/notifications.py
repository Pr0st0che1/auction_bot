from django.conf import settings
import requests

def send_telegram_message(user, message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = user.telegram_chat_id  # Получаем chat_id пользователя
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

def notify_lot_winner(lot):
    highest_bid = Bid.objects.filter(lot=lot).order_by('-amount').first()
    if highest_bid:
        send_telegram_message(
            highest_bid.user,
            f"Поздравляем! Вы выиграли аукцион на лот '{lot.name}' за {highest_bid.amount}."
        )