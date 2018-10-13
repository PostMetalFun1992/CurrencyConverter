from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.response import Response

from converter_app.serializers import CurrencyConversationSerializer
from converter_app.utils import convert_amount


class CurrencyConversationView(generics.GenericAPIView):
    serializer_class = CurrencyConversationSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        converted_amount = convert_amount(**serializer.data)
        if converted_amount:
            return Response({
                **serializer.data,
                **{'converted_amount': converted_amount}
            })

        return Response(
            'Cannot found rates: {}-{}'
            .format(
                request.data['base_currency'],
                request.data['convertible_currency']
            ),
            status=status.HTTP_404_NOT_FOUND
        )
