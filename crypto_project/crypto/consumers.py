import json
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"


class CryptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle new client connection"""
        await self.channel_layer.group_add("crypto_prices", self.channel_name)
        await self.accept()
        self.binance_task = asyncio.create_task(self.receive_binance_data())

    async def disconnect(self, close_code):
        """Handle client disconnection"""
        await self.channel_layer.group_discard(
            "crypto_prices", self.channel_name
        )
        if hasattr(self, "binance_task"):
            self.binance_task.cancel()

    async def receive_binance_data(self):
        """Receive data from Binance WebSocket"""
        last_price = None
        try:
            async with websockets.connect(BINANCE_WS_URL) as ws:
                while True:
                    if last_price is None:
                        data = json.loads(await ws.recv())
                        last_price = float(data["p"])
                        timestamp = data["T"]

                    await self.channel_layer.group_send(
                        "crypto_prices",
                        {
                            "type": "send_price_update",
                            "data": {
                                "symbol": "BTC/USDT",
                                "price": last_price,
                                "timestamp": timestamp,
                            },
                        },
                    )

                    await asyncio.sleep(1)
                    last_price = None
        except Exception as e:
            logger.error(f"Error in receive_binance_data: {e}")

    async def send_price_update(self, event):
        """Send price update to client"""
        await self.send(text_data=json.dumps(event["data"]))
