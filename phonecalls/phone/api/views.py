from rest_framework import generics
from phone.api.serializers import CallDetailSerializer


class PhoneCallAdd(generics.CreateAPIView):
    """
        post:
           Create the new phone call registry.
           Case type_call is 'start' source and
           destination is required.
    """
    serializer_class = CallDetailSerializer
