from django.urls import path
from wallet.api import views

app_name = 'wallet_api'

urlpatterns = [
    path('create_wallet/',views.create_wallet, name='create_wallet'),
    path('get_balance/',views.get_balance, name='get_balance'),
    path('update_balance/',views.update_balance, name='update_balance'),
    path('convert_currency/',views.convert_currency, name='convert_currency'),
    path('transfer/',views.transfer_money, name='transfer_money'),
    path('invoice/<id>/',views.generate_pdf, name='generate_pdf'),
    path('transaction/',views.generate_transaction_pdf, name='generate_transaction_pdf'),
    path('send_monthly_email/',views.send_monthly_email, name='send_monthly_email'),
]
