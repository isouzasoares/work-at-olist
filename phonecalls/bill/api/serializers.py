from rest_framework import serializers
from bill.models import BillCall


class BillCallSerializer(serializers.ModelSerializer):
    call_duration = serializers.SerializerMethodField()
    call_price = serializers.SerializerMethodField()

    class Meta:
        model = BillCall
        fields = ('call_id', 'call_start_date', 'call_start_time',
                  'call_duration', 'call_price')

    def get_call_duration(self, obj):
        seconds = obj.call_duration.total_seconds()
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return '%dh%02dm%02ds' % (hours, mins, secs)

    def get_call_price(self, obj):
        return "R$ %s" % (str(obj.call_price).replace(".", ","))
