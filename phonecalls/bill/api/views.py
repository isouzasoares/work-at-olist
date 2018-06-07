from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from bill.models import BillCall
from bill.utils import get_month_year
from bill.api.serializers import BillCallSerializer, MonthYearFilter
from phone.models import Phone
from phone.api.serializers import PhoneSerializer


class BillDetailList(ListAPIView):
    """
        get:
            return a telephone bill the last closed period.
            The month_year parameter is not required and your format is m/Y.
            It's only possible to get a telephone bill after
            the reference period has ended.

    """
    queryset = BillCall.objects.all()
    serializer_class = BillCallSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MonthYearFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            call_id__source__number=self.kwargs["source_number"])
        return qs

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except ValueError:
            return Response({"Date format is m/Y"},
                            status=status.HTTP_400_BAD_REQUEST)

        if queryset:
            month_year = get_month_year(request.GET.get("month_year"))
            month_year = month_year.strftime("%m/%Y")
            serializer = self.get_serializer(queryset, many=True)
            data = PhoneSerializer(Phone.objects.get(
                number=kwargs["source_number"])).data
            data["period"] = month_year
            data["call_records"] = serializer.data
            return Response(data)

        return Response({})
