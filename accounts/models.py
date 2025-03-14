from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Order(models.Model):
    SERVICE_CHOICES = [
        ("tiktok", "TikTok"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
    ]
    BOOST_TYPES = [
        ("views", "Просмотры"),
        ("followers", "Подписчики"),
        ("likes", "Лайки"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    link = models.URLField()
    boost_type = models.CharField(max_length=20, choices=BOOST_TYPES)
    amount = models.IntegerField()
    progress = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service} - {self.amount}"
