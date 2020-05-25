from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0, blank=True)
    currency = models.CharField(max_length=3, blank=True, default='inr')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=20)
    sender_currency = models.CharField(max_length=3)
    receiver = models.CharField(max_length=20)
    receiver_currency = models.CharField(max_length=3)
    amount = models.FloatField()
    exchange_rate = models.FloatField()

    def __str__(self):
        return str(self.transaction_id)