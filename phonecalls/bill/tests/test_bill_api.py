from datetime import time, timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from rest_framework.test import APIRequestFactory
from phone.models import Call, Phone
from bill.models import BillCall


class BillDetailApiTestCase(TestCase):
    client = APIRequestFactory()

    def setUp(self):
        phone = Phone.objects.create(number="31985853903")
        phone2 = Phone.objects.create(number="31985853901")
        call = Call.objects.create(source=phone,
                                   destination=phone2,
                                   call_id=70)
        date_test = timezone.datetime(2017, 5, 23, 22, 00, 00,
                                      tzinfo=timezone.get_current_timezone())
        BillCall.objects.create(call_id=call,
                                call_start_date=date_test.date(),
                                call_start_time=time(22, 00),
                                call_duration=timedelta(hours=0,
                                                        minutes=10,
                                                        seconds=0),
                                call_price=1.26)
        call2 = Call.objects.create(source=phone,
                                    destination=phone2,
                                    call_id=71)
        date_test = timezone.datetime(2017, 5, 25, 10, 15, 20,
                                      tzinfo=timezone.get_current_timezone())
        BillCall.objects.create(call_id=call2,
                                call_start_date=date_test.date(),
                                call_start_time=time(10, 15, 20),
                                call_duration=timedelta(hours=35,
                                                        minutes=10,
                                                        seconds=25),
                                call_price=300.50)
        call3 = Call.objects.create(source=phone2,
                                    destination=phone,
                                    call_id=72)

        BillCall.objects.create(call_id=call3,
                                call_start_date=date_test.date(),
                                call_start_time=time(10, 15, 20),
                                call_duration=timedelta(hours=35,
                                                        minutes=10,
                                                        seconds=25),
                                call_price=300.50)

    def test_detail_url(self):
        with self.assertRaises(NoReverseMatch):
            reverse("bill:bill_detail_list")
        with self.assertRaises(NoReverseMatch):
            reverse("bill:bill_detail_list", kwargs={"source_number": "abc"})
        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31985853903"})
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_detail_items(self):
        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31985853903"})
        data = [{'call_id': 70,
                 'call_start_date': '2017-05-23',
                 'call_start_time': '22:00:00',
                 'call_price': 'R$ 1,26',
                 'call_duration': '0h10m00s'},
                {'call_id': 71,
                 'call_start_date': '2017-05-25',
                 'call_start_time': '10:15:20',
                 'call_price': 'R$ 300,50',
                 'call_duration': '35h10m25s'}]

        items = self.client.get(url).json()
        self.assertEqual(data, items)
        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31988888888"})
        items = self.client.get(url).json()
        self.assertEqual([], items)
