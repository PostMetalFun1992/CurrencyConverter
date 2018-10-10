from rest_framework import generics, status
from rest_framework.response import Response

from converter_app.serializers import CurrencyConversationSerializer


class CurrencyConversationView(generics.GenericAPIView):
    serializer_class = CurrencyConversationSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
