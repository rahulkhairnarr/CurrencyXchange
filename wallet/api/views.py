from rest_framework.response import Response
from django.http import HttpResponse
from wallet.api.serializer import WalletSerializer, WalletUpdateSerializer, TransactionSerializer
from wallet.models import Wallet, Transaction
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from xhtml2pdf import pisa
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings



@api_view(['GET', ])
def create_wallet(request):
    user = request.user
    wallet, create = Wallet.objects.get_or_create(user=user)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def get_balance(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Wallet.DoesNotExist as e:
        return Response({"message": "Wallet Does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
def update_balance(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist as e:
        return Response({"message": "Wallet Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        serializer = WalletUpdateSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'],)
def convert_currency(request):
    if "from" in request.data:
        from_currency = request.data['from']
    else:
        data = {"message": "Base currency required"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if "to" in request.data:
        to_currency = request.data['to']
    else:
        data = {"message": "Output currency required"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if "amount" in request.data:
        amount = request.data['amount']
    else:
        data = {"message": "Conversion amount required"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    currency_rates = get_currency_value(from_currency)

    if "rates" in currency_rates:
        if to_currency.upper() in currency_rates['rates']:
            conversion_value = currency_rates['rates'][to_currency.upper(
            )] * float(amount)
            data = {
                "base_currency": from_currency.upper(),
                "base_amt": amount,
                "converted_currency": to_currency.upper(),
                "converted_amt": conversion_value
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'error': "Output Currency Does not Support"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(currency_rates, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'],)
def transfer_money(request):
    # Get Sender Details
    sender = request.user
    api_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    domain_name = 'localhost:8000'

    # Check Required Data Send or Not
    if "receiver" not in request.data:
        data = {"message": "Receiver Username required"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    elif "amount" not in request.data:
        data = {"message": "Transfer Amount required"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # Check weather receiver exist or not
    if check_receiver_exist(request.data['receiver']):
        receiver_user = User.objects.get(username=request.data['receiver'])
        if receiver_user == sender:
            data = {"message": "Invalid Transaction"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"message": "Invalid Receiver Username"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # Check receiver has wallet or not
    if check_wallet_exist(receiver_user):
        receiver_wallet = Wallet.objects.get(user=receiver_user)
    else:
        data = {"message": "Receiver has no wallet"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # Check Send has sufficent balance or not
    transfer_amount = float(request.data['amount'])
    if check_sufficent_balance(sender, transfer_amount):
        sender_wallet = Wallet.objects.get(user=sender)
    else:
        data = {"message": "You have insufficent balance"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # Get Latest Currency Price
    exchange_rates = get_currency_value(sender_wallet.currency)

    if "rates" in exchange_rates:

        if receiver_wallet.currency.upper() in exchange_rates['rates']:
            exchange_rate = exchange_rates['rates'][receiver_wallet.currency.upper(
            )]
            converted_amt = exchange_rate * float(transfer_amount)
        else:
            data = {'error': "Output Currency Does not Support"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(exchange_rates, status=status.HTTP_404_NOT_FOUND)

    transancation = Transaction(sender=sender,
                                sender_currency=sender_wallet.currency,
                                receiver_currency=receiver_wallet.currency,
                                exchange_rate=exchange_rate)

    transanction_serializer = TransactionSerializer(
        transancation, data=request.data)
    if transanction_serializer.is_valid():
        transanction_serializer.save()

        # Add Money to Receiver Account
        receiver_wallet.balance += converted_amt
        receiver_wallet.save()

        # Deducte Money from Sender Account
        sender_wallet.balance -= float(transfer_amount)
        sender_wallet.save()
        transaction_id = transanction_serializer.data['transaction_id']
        data = {}
        data['invoiceUrl'] = 'http://%s/api/invoice/%s/?token=%s' % (
            domain_name, transaction_id, api_token)
        data.update(transanction_serializer.data)
        return Response(data, status=status.HTTP_200_OK)

    else:
        data = {'error': "Output Currency Does not Support"}
        return Response(data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'],)
@permission_classes([AllowAny])
def generate_pdf(request, id):
    token = request.GET.get('token', '')
    user = Token.objects.get(key=token)
    if token != '':
        template_path = 'receipt.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Receipt.pdf"'

        transaction = Transaction.objects.get(transaction_id=id)
        if user.user is transaction.sender:
            data = {'error': "Unauthorized Access"}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        html = render_to_string(template_path, {'transaction': transaction})
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
    else:
        data = {'error': "Authentication Token not found"}
        return Response(data, status=status.HTTP_404_NOT_FOUND)


def check_receiver_exist(receiver_username):
    try:
        receiver_user = User.objects.get(username=receiver_username)
        return True
    except User.DoesNotExist:
        return False


def check_wallet_exist(receiver):
    try:
        wallet = Wallet.objects.get(user=receiver)
        return True
    except Wallet.DoesNotExist:
        return False


def check_sufficent_balance(sender, transfer_amount):
    wallet = Wallet.objects.get(user=sender)
    if wallet.balance >= float(transfer_amount):
        return True
    else:
        return False


def get_currency_value(base_currency):
    url = 'https://api.exchangeratesapi.io/latest?base=' + base_currency.upper()
    response = requests.get(url)
    response = response.json()
    return response


@api_view(['GET'],)
@permission_classes([AllowAny])
def generate_transaction_pdf(request):

    token = request.GET.get('token', '')
    user = Token.objects.get(key=token)
    if token != '':
        template_path = 'transaction_details.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Tranaction Details.pdf"'

        current_time = datetime.today()
        transactions = Transaction.objects.filter(
            sender=user.user, create_at__month=(current_time.month - 1))
        wallet = Wallet.objects.get(user=user.user)

        html = render_to_string(template_path, {
                                'transactions': transactions, 'wallet': wallet, 'month': current_time.strftime('%B')})
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
    else:
        data = {'error': "Authentication Token not found"}
        return Response(data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'],)
@permission_classes([AllowAny])
def send_monthly_email(request):
    domain_name = request.META['HTTP_HOST']
    statement_url = 'http://%s/api/transaction/?token=' % (domain_name)
    tokens = Token.objects.all()

    email_subject = 'Monthly Transaction Statement'
    for token in tokens:
        statement_url = 'http://%s/api/transaction/?token=%s' % (
            domain_name, token)
        user = User.objects.get(username=token.user)

        html_content = "<p><strong>Monthly Transaction Statement</strong></p>"
        html_content += "<p><a href=" + \
            statement_url + ">Download File</a></p><br><br>"
        email_id = user.email

        text_content = strip_tags(html_content)
        subject, from_email, to = email_subject, settings.EMAIL_HOST_USER, email_id
        try:
            msg = EmailMultiAlternatives(
                subject=subject, body=text_content, from_email=from_email, to=[to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            data = {'error': e}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


    data = {'status': "success"}
    return Response(data, status=status.HTTP_200_OK)