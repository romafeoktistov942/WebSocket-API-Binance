import pytest
from decimal import Decimal
from crypto.models import CryptoPrice


@pytest.mark.django_db
class TestCryptoPrice:
    def test_create_crypto_price(self):
        """Test creating a new CryptoPrice instance"""
        price = CryptoPrice.objects.create(
            symbol="BTC/USDT", price=Decimal("50000.00")
        )
        assert price.symbol == "BTC/USDT"
        assert price.price == Decimal("50000.00")
        assert price.timestamp is not None

    def test_crypto_price_ordering(self):
        """Test that CryptoPrice objects are ordered by timestamp descending"""
        first = CryptoPrice.objects.create(
            symbol="BTC/USDT", price=Decimal("50000.00")
        )
        second = CryptoPrice.objects.create(
            symbol="BTC/USDT", price=Decimal("51000.00")
        )
        prices = CryptoPrice.objects.all()
        assert prices[0] == second
        assert prices[1] == first
