import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from crypto.price_service import PriceService
from crypto.models import CryptoPrice
import json


@pytest.mark.asyncio
class TestPriceService:
    async def test_service_initialization(self):
        """Test PriceService initialization"""
        service = PriceService()
        assert service.running is False
        assert service.last_price is None
        assert service.first_price_saved is False

    @patch("websockets.connect")
    async def test_fetch_prices(self, mock_connect):
        """Test fetching prices from WebSocket"""
        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(
            return_value=json.dumps({"p": "50000.00", "T": 1234567890})
        )
        mock_connect.return_value.__aenter__.return_value = mock_ws

        service = PriceService()
        service.running = True

        task = asyncio.create_task(service.fetch_prices())
        await asyncio.sleep(0.1)
        service.running = False
        await task

        assert service.last_price == 50000.00

    @pytest.mark.django_db
    async def test_save_to_db(self):
        """Test saving prices to database"""
        service = PriceService()
        await service.save_to_db("BTC/USDT", 50000.00)

        saved_price = await CryptoPrice.objects.afirst()
        assert saved_price is not None
        assert saved_price.symbol == "BTC/USDT"
        assert float(saved_price.price) == 50000.00
