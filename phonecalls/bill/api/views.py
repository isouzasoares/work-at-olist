from dateutil.relativedelta import relativedelta
from django.utils import timezone

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from bill.models import BillCall
from bill.api.serializers import BillCallSerializer
from phone.choices import END


class BillDetailList(ListAPIView):
    queryset = BillCall.objects.all()
    serializer_class = BillCallSerializer

    def list(self, request, *args, **kwargs):
        now = timezone.now().replace(day=1).date()
        month_year = request.GET.get("month_year", None)
        queryset = self.filter_queryset(self.get_queryset())

        if not month_year:
            month_year = now - relativedelta(months=1)
        else:
            try:
                month_year = timezone.datetime.strptime(month_year, "%m/%Y")
                month_year = month_year.date()
            except ValueError:
                return Response({"Date format is m/Y"},
                                status=status.HTTP_400_BAD_REQUEST)

        month_year = month_year.replace(day=1)
        if month_year < now:
            queryset = queryset.filter(
                call_id__source__number=kwargs["source_number"],
                call_id__calldetail__type_call=END,
                call_id__calldetail__timestamp__month=month_year.month,
                call_id__calldetail__timestamp__year=month_year.year)
            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)

        return Response([])
