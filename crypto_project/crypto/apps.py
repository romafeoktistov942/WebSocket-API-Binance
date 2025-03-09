from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class CryptoConfig(AppConfig):
    """
    Configuration class for the crypto app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "crypto"

    def ready(self):
        """
        Starts the price service when the main process is running.
        """
        import os

        if os.environ.get("RUN_MAIN") or os.environ.get("DAPHNE"):
            from .price_service import start_price_service

            start_price_service()
            logger.info("PriceService started via apps.py")
