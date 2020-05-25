from rest_framework import serializers
from wallet.models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'currency', 'update_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'receiver', 'amount']