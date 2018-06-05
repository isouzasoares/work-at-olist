from rest_framework import serializers
from django_filters import rest_framework as filters

from phone.choices import END
from bill.models import BillCall
from bill.utils import get_month_year


class BillCallSerializer(serializers.ModelSerializer):
    """Serialization for BillCall.

    :param call_id: Call id pk.
    :type call_id: int

    :param call_start_date: Date of starts the call
    :type call_start_date: str

    :param call_start_time: hour, minutes, seconds from
                            the beginning of the call
    :type call_start_time: str

    :param call_duration: call duration
    :type call_duration: str

    :param call_price: call price
    :type call_price: str

    """
    call_duration = serializers.SerializerMethodField()
    call_price = serializers.SerializerMethodField()

    class Meta:
        model = BillCall
        fields = ('call_id', 'call_start_date', 'call_start_time',
                  'call_duration', 'call_price')

    def get_call_duration(self, obj):
        """Add mask to call_duration and
        return for serializer field call_duration

        :returns: total time format 00h00m00s
        :rtype: str
        """
        seconds = obj.call_duration.total_seconds()
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return '%dh%02dm%02ds' % (hours, mins, secs)

    def get_call_price(self, obj):
        """Replace . and add mask to call_price and
        return for serializer field call_price

        :returns: price format R$ 00,0
        :rtype: str
        """
        return "R$ %s" % (str(obj.call_price).replace(".", ","))


class MonthYearFilter(filters.FilterSet):
    """Serialization for MonthYear, django-filter
       format

    :param month_year: month_year.
    :type month_year: str, format %d/%Y

    """
    month_year = filters.CharFilter()

    class Meta:
        model = BillCall
        fields = ("month_year",)

    @property
    def qs(self):
        """Returns django filter queryset.

        """
        month_year = self.data.get('month_year')
        try:
            month_year = get_month_year(month_year)
        except ValueError:
            raise ValueError

        if month_year:
            queryset = self.queryset.filter(
                call_id__calldetail__type_call=END,
                call_id__calldetail__timestamp__month=month_year.month,
                call_id__calldetail__timestamp__year=month_year.year)
        else:
            queryset = self.queryset.none()

        return queryset
