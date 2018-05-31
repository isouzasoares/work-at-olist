from rest_framework.generics import ListAPIView

from bill.models import BillCall
from bill.api.serializers import BillCallSerializer


class BillDetailList(ListAPIView):
    lookup_field = "call_id__destination__number"
    lookup_url_kwarg = "source_number"
    queryset = BillCall.objects.all()
    serializer_class = BillCallSerializer
