import asyncio
import json
import websockets
import logging
import threading
from django.utils.timezone import now
from channels.db import database_sync_to_async
from .models import CryptoPrice

logger = logging.getLogger(__name__)


def start_price_service():
    """
    Initialize and start the PriceService in a separate thread.
    Creates a new event loop and runs the service continuously.
    """
    if not hasattr(start_price_service, "is_running"):
        start_price_service.is_running = True

        def run_service():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            service = PriceService()
            loop.run_until_complete(service.start())
            loop.run_forever()

        thread = threading.Thread(target=run_service, daemon=True)
        thread.start()
        logger.info("PriceService thread started")


class PriceService:
    """
    A service that connects to Binance WebSocket API to fetch real-time
    cryptocurrency prices and store them in the database.

    The service maintains a continuous WebSocket connection and saves price
    data periodically while ensuring the first price is saved immediately
    upon receiving.
    """

    def __init__(self):
        """Initialize the PriceService with default configuration."""
        self.ws_url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
        self.running = False
        self.last_price = None
        self.first_price_saved = False

    async def start(self):
        """
        Start the price service by initializing price fetching and
        periodic saving.

        Raises:
            Exception: If there's an error during service startup
        """
        if self.running:
            return

        try:
            self.running = True
            await asyncio.gather(self.fetch_prices(), self.periodic_save())
        except Exception as e:
            self.running = False
            logger.error(f"Error starting PriceService: {e}")
            raise

    async def fetch_prices(self):
        """
        Continuously fetch prices from Binance WebSocket API.
        Saves the first received price and updates the last_price
        for periodic saving.
        """
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    while self.running:
                        data = json.loads(await ws.recv())
                        self.last_price = float(data["p"])

                        if (
                            not self.first_price_saved
                            and self.last_price is not None
                        ):
                            await self.save_to_db("BTC/USDT", self.last_price)
                            self.first_price_saved = True
                            logger.info("Initial price saved")
            except Exception as e:
                logger.error(f"Price fetching error: {e}")
                await asyncio.sleep(5)

    async def periodic_save(self):
        """
        Periodically save the last known price to the database.
        Executes every 60 seconds if a price is available.
        """
        while self.running:
            try:
                await asyncio.sleep(60)
                if self.last_price is not None:
                    await self.save_to_db("BTC/USDT", self.last_price)
            except Exception as e:
                logger.error(f"Periodic save error: {e}")

    @database_sync_to_async
    def save_to_db(self, symbol: str, price: float) -> None:
        """
        Save the price data to the database.

        Args:
            symbol (str): The trading pair symbol
            price (float): The current price
        """
        CryptoPrice.objects.create(symbol=symbol, price=price, timestamp=now())
