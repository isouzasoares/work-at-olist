from datetime import datetime, time
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory
from phone.choices import START, END
from bill.models import BillCall


class PhoneCallApiTestCase(TestCase):
    client = APIRequestFactory()

    def test_post_calldetail(self):
        url = reverse("phone-api:call_add")
        data = {"call_id": 75,
                "timestamp": "2018-05-01 21:57:13",
                "type_call": START,
                "source": "31985853903",
                "destination": "3188888888"}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

        data = {"call_id": 75,
                "timestamp": "2018-05-01 22:10:56",
                "type_call": END}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

        billcall = BillCall.objects.get(call_id_id=75)
        self.assertEqual(billcall.call_start_date,
                         datetime(2018, 5, 1).date())
        self.assertEqual(billcall.call_price,
                         Decimal("0.54"))
        self.assertEqual(billcall.call_start_time,
                         time(21, 57, 13))

    def test_call_post_validate_test(self):
        url = reverse("phone-api:call_add")
        data = {"call_id": 75,
                "timestamp": "2018-05-01 20:00:00",
                "type_call": START,
                "source": "31985853903",
                "destination": "31985853903"}
        request = self.client.post(url, data).json()
        error = {'non_field_errors': ['source and destination are identical']}
        self.assertEqual(request, error)

        data = {"call_id": 75,
                "timestamp": "2018-05-01 20:00:00",
                "type_call": START}
        request = self.client.post(url, data).json()
        error = {'non_field_errors':
                 ['For type_call start, source and destination is required']}
        self.assertEqual(request, error)

        data = {"call_id": 75,
                "timestamp": "2018-05-02 22:00:00",
                "type_call": START,
                "source": "31985853903",
                "destination": "3188888888"}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

        data = {"call_id": 75,
                "timestamp": "2018-05-01 21:00:00",
                "type_call": END}
        request = self.client.post(url, data).json()
        error = {'timestamp':
                 ['Timestamp start call is > to timestamp']}
        self.assertEqual(request, error)

        data = {"call_id": 80,
                "timestamp": "2018-05-01 23:00:00",
                "type_call": END}
        request = self.client.post(url, data).json()
        error = {'call_id':
                 ['call_id does not exists. Please create call start']}
        self.assertEqual(request, error)
