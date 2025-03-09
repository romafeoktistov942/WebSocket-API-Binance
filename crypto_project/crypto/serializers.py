from rest_framework import serializers
from .models import CryptoPrice


class CryptoPriceSerializer(serializers.ModelSerializer):
    """
    Serializer for the CryptoPrice model.
    """

    class Meta:
        model = CryptoPrice
        fields = ["symbol", "price", "timestamp"]
