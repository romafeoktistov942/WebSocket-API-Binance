import pytest
from channels.testing import WebsocketCommunicator
from crypto_project.asgi import application


@pytest.mark.asyncio
class TestCryptoConsumer:
    @pytest.mark.django_db
    async def test_connection(self):
        """Test WebSocket connection"""
        communicator = WebsocketCommunicator(application, "/ws/prices/")
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    @pytest.mark.django_db
    @pytest.mark.asyncio
    async def test_receive_messages(self):
        """Test receiving messages from WebSocket"""
        communicator = WebsocketCommunicator(application, "/ws/prices/")
        connected, _ = await communicator.connect()
        assert connected

        response = await communicator.receive_json_from(timeout=5.0)
        assert "symbol" in response
        assert "price" in response
        assert "timestamp" in response
        assert response["symbol"] == "BTC/USDT"

        await communicator.disconnect()
