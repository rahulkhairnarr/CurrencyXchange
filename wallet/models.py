from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0, blank=True)
    currency = models.CharField(max_length=3, blank=True, default='inr')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

