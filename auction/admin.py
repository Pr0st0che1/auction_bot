from django.contrib import admin
from django.utils.timezone import now
from .models import User, Lot, Bid, Image, Purchase, Strike, Complaint
from .auction_logic import close_auction  # ✅ Добавляем импорт логики закрытия аукциона

# Декоратор для отображения активности лота
@admin.display(boolean=True, description='Активен ли лот?')
def is_active_status(obj):
    """Проверка, активен ли лот (текущая дата между временем начала и окончания)"""
    return obj.start_time <= now() <= obj.end_time

# Декоратор для действия, чтобы закрывать завершенные лоты
@admin.action(description='Закрыть завершенные лоты')
def close_completed_lots(modeladmin, request, queryset):
    """Закрывает все завершенные лоты, меняя их статус"""
    queryset.update(status='completed', end_time=now())

# Декоратор для закрытия аукциона вручную через админку
@admin.action(description='Завершить выбранные аукционы')
def close_selected_auctions(modeladmin, request, queryset):
    """Завершает аукцион с автоматической проверкой победителя"""
    for lot in queryset:
        result = close_auction(lot)
        modeladmin.message_user(request, result)

# Модель для User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'balance', 'successful_bids', 'auto_bid_access')
    list_filter = ('role',)
    search_fields = ('username', 'email')

# Модель для Lot
@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting_price', 'status', 'is_active_status', 'start_time', 'end_time')
    list_filter = ('status',)
    search_fields = ('name', 'description')
    actions = [close_completed_lots, close_selected_auctions]  # ✅ Добавлено действие закрытия аукциона вручную

    # Добавляем проверку активности лота в админке
    def is_active_status(self, obj):
        return is_active_status(obj)

# Модель для Bid
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('lot', 'user', 'amount', 'timestamp')
    list_filter = ('lot', 'user')
    search_fields = ('lot__name', 'user__username')

# Модель для Image
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)

# Модель для Purchase
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('lot', 'buyer', 'final_price', 'timestamp')
    search_fields = ('lot__name', 'buyer__username')

# Модель для Strike
@admin.register(Strike)
class StrikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'timestamp')
    search_fields = ('user__username',)

# Модель для Complaint
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_admin', 'timestamp', 'text')
    search_fields = ('user__username', 'target_admin__username', 'text')
