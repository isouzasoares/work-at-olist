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

        # test inserts
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

        date = "2016-02-29T12:00:00Z"
        data = {'call_id': 77,
                'source': '99988526423',
                'destination': '9993468278',
                'type_call': 'start',
                'timestamp': date}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

        date = "2018-03-01T22:10:56Z"
        data = {'call_id': 77,
                'type_call': 'end',
                'timestamp': date}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

    def test_call_post_validate_test(self):

        # test errors
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
                "timestamp": "2018-05-02 22:00:00",
                "type_call": END,
                "source": "31985853903",
                "destination": "3188888888"}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

        data = {"call_id": 74,
                "timestamp": "2018-05-02 22:00:00",
                "type_call": START,
                "source": "31985853903",
                "destination": "3188888888"}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

        data = {"call_id": 74,
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

        data = {"call_id": 75,
                "timestamp": "2018-05-02 22:00:00",
                "type_call": START,
                "source": "31985853903",
                "destination": "3188888888"}
        request = self.client.post(url, data).json()
        error = {'call_id':
                 ['call_id already exists for type_call']}
        self.assertEqual(request, error)

        # test phone regex
        data = {"call_id": 78,
                "timestamp": "2018-05-02 22:00:00",
                "type_call": START,
                "source": "3198585390A",
                "destination": "318888888A"}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 400)

        # test phone regex
        data = {"call_id": 78,
                "timestamp": "2018-05-02 22:00:00",
                "type_call": START,
                "source": "3192683903",
                "destination": "31988888888"}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)
