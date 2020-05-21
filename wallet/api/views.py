from rest_framework.response import Response
from wallet.api.serializer import WalletSerializer, WalletUpdateSerializer
from wallet.models import Wallet
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import requests

@api_view(['GET',])
def create_wallet(request):
    user = request.user
    wallet, create = Wallet.objects.get_or_create(user=user)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET',])
def get_balance(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Wallet.DoesNotExist as e:
        return Response({"message": "Wallet Does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT',])
def update_balance(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist as e:
        return Response({"message": "Wallet Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    print(wallet)
    if request.method == "PUT":
        serializer = WalletUpdateSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # data = {"message": "Wallet Does not exist"}
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

    url = 'https://api.exchangeratesapi.io/latest?base='+ from_currency.upper()
    response = requests.get(url)
    response = response.json()
    if "rates" in response:
        if to_currency.upper() in response['rates']:        
            conversion_value = response['rates'][to_currency.upper()] * float(amount)
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
        data = response
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
