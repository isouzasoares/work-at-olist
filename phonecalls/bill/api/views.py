from rest_framework.generics import ListAPIView

from bill.models import BillCall
from bill.api.serializers import BillCallSerializer


class BillDetailList(ListAPIView):
    queryset = BillCall.objects.all()
    serializer_class = BillCallSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            call_id__source__number=self.kwargs["source_number"])
        return qs
