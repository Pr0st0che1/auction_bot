from django.utils import timezone
from .models import Lot, Bid, User, Purchase


# Функция для размещения ставки
def place_bid(user, lot, bid_amount):
    if lot.status != 'on_auction':
        return "Лот уже завершен или продан."

    highest_bid = Bid.objects.filter(lot=lot).order_by('-amount').first()
    if highest_bid and bid_amount <= highest_bid.amount:
        return f"Ваша ставка должна быть больше текущей ({highest_bid.amount})"

    bid = Bid.objects.create(lot=lot, user=user, amount=bid_amount)
    return f"Ваша ставка на лот '{lot.name}' успешно размещена."


# Функция для завершения аукциона
def close_auction(lot):
    if lot.status == 'completed':
        return "Аукцион для этого лота уже завершен."

    highest_bid = Bid.objects.filter(lot=lot).order_by('-amount').first()

    if highest_bid:
        lot.status = 'sold'
        lot.save()
        Purchase.objects.create(lot=lot, buyer=highest_bid.user, final_price=highest_bid.amount)
        return f"Лот '{lot.name}' продан за {highest_bid.amount} пользователю {highest_bid.user.username}"

    lot.status = 'completed'
    lot.save()
    return f"Лот '{lot.name}' не был продан. Аукцион завершен."


# Функция для автоматической ставки
def place_auto_bid(user, lot):
    if not user.auto_bid_access:
        return "У вас нет доступа к автоставкам."

    highest_bid = Bid.objects.filter(lot=lot).order_by('-amount').first()
    if not highest_bid:
        return "Нет ставок на этот лот."

    new_bid_amount = highest_bid.amount + 1
    return place_bid(user, lot, new_bid_amount)


def check_lot_expiration():
    ongoing_lots = Lot.objects.filter(status='on_auction')
    for lot in ongoing_lots:
        if timezone.now() >= lot.end_time:
            close_auction(lot)