from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    BALANCE_THRESHOLD = 500
    SUCCESSFUL_BIDS_THRESHOLD = 10

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'SuperAdmin'),
        ('support', 'Support'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    successful_bids = models.IntegerField(default=0)
    auto_bid_access = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='auction_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='auction_user_permissions_set',
                                              blank=True)

    def save(self, *args, **kwargs):
        # Автоматическое предоставление доступа к автоставкам при достижении условий
        if self.balance >= self.BALANCE_THRESHOLD or self.successful_bids >= self.SUCCESSFUL_BIDS_THRESHOLD:
            self.auto_bid_access = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Image(models.Model):
    # Модель для хранения изображений лотов
    image = models.ImageField(upload_to='lot_images/')

    def __str__(self):
        return f"Image {self.id}"

class Lot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на пользователя-продавца
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('on_auction', 'На аукционе'), ('sold', 'Продано'), ('completed', 'Завершено')])
    location = models.CharField(max_length=255)
    images = models.ManyToManyField('Image', blank=True)  # Множество изображений лота

    def __str__(self):
        return self.name

    def is_active(self):
        """Проверка, активен ли лот на аукционе"""
        now = timezone.now('2025-03-20 12:00:00')
        if self.start_time <= now <= self.end_time and self.status == 'on_auction':
            return True
        return False

    def is_sold(self):
        """Проверка, продан ли лот"""
        return self.status == 'sold'

    def is_completed(self):
        """Проверка, завершен ли аукцион"""
        return self.status == 'completed'

    def time_left(self):
        """Возвращает оставшееся время до окончания аукциона"""
        if self.is_active():
            remaining_time = self.end_time - timezone.now()
            return remaining_time
        return None

class Bid(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f'{self.user} bid for {self.lot}'

class Purchase(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} купил {self.lot.name} за {self.final_price}"

class Strike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Страйк для {self.user.username}: {self.reason}"

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_received')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Жалоба на {self.target_admin.username} от {self.user.username}"
