from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from phone.models import CallDetail, Phone, Call
from phone.choices import START, END, TYPE_CALL_CHOICES

REGEX_NUMBER = r"^\d{10,11}"


class CallDetailSerializer(serializers.Serializer):
    """Serialization for CallDetail.

    :param call_id: Call id pk.
    :type call_id: int

    :param source: number source call
    :type source: str numbers, min lenght 10, max_length 11

    :param destination: number destination call
    :type destination: str number, min lenght 10, max_length 11

    :param type_call: number destination call
    :type type_call: str choices, start or end

    :param timestamp: the datetime starts or ends call
    :type timestamp: str

    """
    call_id = serializers.IntegerField()
    source = serializers.RegexField(REGEX_NUMBER,
                                    min_length=10, max_length=11,
                                    required=False)
    destination = serializers.RegexField(REGEX_NUMBER,
                                         min_length=10, max_length=11,
                                         required=False)
    type_call = serializers.ChoiceField(choices=TYPE_CALL_CHOICES)
    timestamp = serializers.DateTimeField()

    def validate(self, data):
        """Returns the validated_data

        :raises: ValidationError

        """
        call = CallDetail.objects.filter(call_id=data["call_id"],
                                         type_call=data["type_call"])
        if call:
            raise serializers.ValidationError(
                {"call_id": "call_id already exists for type_call"})

        if data["type_call"] == END:

            try:
                call = CallDetail.objects.get(call_id=data["call_id"],
                                              type_call=START)

                if call.timestamp > data["timestamp"]:
                    raise serializers.ValidationError(
                        {"timestamp":
                         "Timestamp start call is > to timestamp"})

            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    {"call_id":
                     "call_id does not exists. Please create call start"})

        if data["type_call"] == START:

            if not data.get("source") or not data.get("destination"):
                raise serializers.ValidationError(
                    "For type_call start, source and destination is required")
            elif data["source"] == data["destination"]:
                raise serializers.ValidationError(
                    "source and destination are identical")

        return data

    def create(self, validated_data):
        """Create the Phone, Destination, Call and
        CallDetail registry

        .. note::
            If type_call == 'start' the source and
            destination is required.

        :returns: validated_data
        :rtype: dict

        """
        call_id = validated_data.get("call_id")
        validated = validated_data.copy()
        source = validated.pop("source", "")
        destination = validated.pop("destination", "")

        if validated_data.get("type_call") == START:
            source, created_source = Phone.objects.get_or_create(number=source)
            destination, created_destination = Phone.objects.get_or_create(
                number=destination)
            call, created = Call.objects.get_or_create(
                call_id=call_id,
                source=source,
                destination=destination)
        else:
            call = Call.objects.get(call_id=call_id)
            validated_data["source"] = call.source.number
            validated_data["destination"] = call.destination.number

        validated["call_id"] = call
        CallDetail.objects.create(**validated)
        return validated_data


class PhoneSerializer(serializers.ModelSerializer):
    """Serialization for Phone.

    :param id: phone pk.
    :type id: int auto_add

    :param number: phone number.
    :type str: min_length 10, max_length 11
    """

    class Meta:
        model = Phone
        fields = ("id", "number")
