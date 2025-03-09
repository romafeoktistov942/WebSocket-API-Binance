from django.db import models


class CryptoPrice(models.Model):
    """
    Model representing the price of a cryptocurrency at a specific timestamp.
    """

    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        """
        Returns a string representation of the CryptoPrice instance.
        """
        return f"{self.symbol}: {self.price} at {self.timestamp}"
