from rest_framework import generics
from phone.api.serializers import CallDetailSerializer


class PhoneCallAdd(generics.ListCreateAPIView):
    serializer_class = CallDetailSerializer
