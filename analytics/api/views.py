from rest_framework.response import Response
from django.http import HttpResponse
from wallet.api.serializer import TransactionSerializer
from wallet.models import  Transaction, Wallet
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.contrib.auth.models import User
from datetime import datetime
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.db.models import Avg, Sum
from wallet.api.views import get_currency_value




@api_view(['GET'],)
def get_pl_details(request):
    user = request.user
    current_date = datetime.today().strftime('%Y-%m-%d')
    from_date = request.data['start_date']
    receiver_currency_list  =[]
    total_pl = 0
    try:
        start_date = datetime.strptime(from_date, '%Y-%m-%d')
    except ValueError:
        data = {'error': "Invalid Date format. Please Enter in YYYY/MM/DD format"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

    wallet = Wallet.objects.get(user=user)
    conversion_rates = get_currency_value(wallet.currency)
    
    transactions = Transaction.objects.filter(create_at__range=[start_date, current_date], sender=user)
    
    for transaction in transactions:
        if transaction.receiver_currency not in receiver_currency_list:
            receiver_currency_list.append(transaction.receiver_currency)

    for currency in receiver_currency_list:
        exchange_avg = Transaction.objects.filter(create_at__range=[start_date, current_date], sender=user, receiver_currency=currency).aggregate(Avg('exchange_rate'))
        # exchange_rate__avg
        total_amt = Transaction.objects.filter(create_at__range=[start_date, current_date], sender=user, receiver_currency=currency).aggregate(Sum('amount'))

        history_rate = exchange_avg['exchange_rate__avg'] * total_amt['amount__sum']
        exchange_rate = conversion_rates['rates'][currency.upper()]
        current_rate_conversion = exchange_rate * total_amt['amount__sum']
        total_pl = total_pl + (history_rate - current_rate_conversion)

    data = {'total_profit_loss': total_pl}
    if total_pl < 0:
        data['type'] = 'Loss'
    else:
        data['type'] = 'Profit'
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'],)
def get_avg_tranfer(request):
    currency_list = []
    transactions = Transaction.objects.all()

    for transaction in transactions:
        if transaction.sender_currency not in currency_list:
            currency_list.append(transaction.sender_currency)
    print(currency_list)
    data = {}
    for day in range(2,7):
        data[day] = {}
        for currency in currency_list:
            total_amt = Transaction.objects.filter(create_at__week_day=day, sender_currency=currency).aggregate(Sum('amount'))
            if total_amt['amount__sum'] is not None:
                data[day][currency] = total_amt['amount__sum']    
    
    return Response(data, status=status.HTTP_200_OK)