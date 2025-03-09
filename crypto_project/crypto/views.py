from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import CryptoPrice
from .serializers import CryptoPriceSerializer


class CryptoPriceListView(APIView):
    """
    API view to retrieve the last 100 cryptocurrency prices.
    """

    @swagger_auto_schema(
        operation_description="Retrieve the last 100 cryptocurrency prices",
        responses={200: CryptoPriceSerializer(many=True)},
    )
    def get(self, request):
        """
        Handle GET request to retrieve the last 100 cryptocurrency prices.
        """
        prices = CryptoPrice.objects.all().order_by("-timestamp")[:100]
        serializer = CryptoPriceSerializer(prices, many=True)
        return Response(serializer.data)
