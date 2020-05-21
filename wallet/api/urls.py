from django.urls import path
from wallet.api.views import create_wallet, get_balance, update_balance, convert_currency

app_name = 'wallet_api'

urlpatterns = [
    path('create_wallet/',create_wallet, name='create_wallet'),
    path('get_balance/',get_balance, name='get_balance'),
    path('update_balance/',update_balance, name='update_balance'),
    path('convert_currency/',convert_currency, name='convert_currency'),
]
