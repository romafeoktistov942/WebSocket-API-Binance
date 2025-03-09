from django.urls import path
from .views import CryptoPriceListView

urlpatterns = [
    path("api/prices/", CryptoPriceListView.as_view(), name="crypto_prices"),
]
