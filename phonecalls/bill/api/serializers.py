from rest_framework import serializers
from bill.models import BillCall


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

        :returns: str, format 00h00m00s
        """
        seconds = obj.call_duration.total_seconds()
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return '%dh%02dm%02ds' % (hours, mins, secs)

    def get_call_price(self, obj):
        """Replace . and add mask to call_price and
        return for serializer field call_price

        :returns: str, format R$ 00,0
        """
        return "R$ %s" % (str(obj.call_price).replace(".", ","))
