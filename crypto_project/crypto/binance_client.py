import asyncio
import websockets
import json
from django.utils.timezone import now
from .models import CryptoPrice

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"


async def binance_listener():
    """
    Listens to the Binance WebSocket for BTC/USDT trade data and
    saves the price to the database.
    """
    async with websockets.connect(BINANCE_WS_URL) as ws:
        while True:
            data = json.loads(await ws.recv())
            price = float(data["p"])
            CryptoPrice.objects.create(
                symbol="BTC/USDT", price=price, timestamp=now()
            )


if __name__ == "__main__":
    asyncio.run(binance_listener())
