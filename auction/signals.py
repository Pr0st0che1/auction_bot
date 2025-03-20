from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Lot, Purchase
import requests
from django.conf import settings

@receiver(post_save, sender=Lot)
def send_auction_end_notification(sender, instance, **kwargs):
    if instance.end_time <= now() and instance.status != 'completed':
        instance.status = 'completed'
        instance.save()

        # Проверяем, есть ли победитель аукциона
        winning_bid = instance.bid_set.order_by('-amount').first()
        if winning_bid:
            Purchase.objects.create(
                lot=instance,
                buyer=winning_bid.user,
                final_price=winning_bid.amount
            )

            # Отправка уведомления через Telegram
            message = (
                f"🏆 Аукцион завершён!\n"
                f"🎯 Лот: {instance.name}\n"
                f"💰 Цена: {winning_bid.amount}\n"
                f"👤 Победитель: {winning_bid.user.username}"
            )
            send_telegram_message(message)

def send_telegram_message(message):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = '1175246479'  # Укажи ID чата, куда отправлять уведомления
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Ошибка отправки уведомления в Telegram: {response.text}")
