from datetime import time, timedelta
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from rest_framework.test import APIRequestFactory
from phone.models import Call, Phone, CallDetail
from phone.choices import END
from bill.models import BillCall


class BillDetailApiTestCase(TestCase):
    client = APIRequestFactory()

    def setUp(self):
        now = timezone.now()
        before = now - relativedelta(months=1)
        phone = Phone.objects.create(number="31985853903")
        phone2 = Phone.objects.create(number="31985853901")
        call = Call.objects.create(source=phone,
                                   destination=phone2,
                                   call_id=70)
        BillCall.objects.create(call_id=call,
                                call_start_date=before.date(),
                                call_start_time=time(22, 00),
                                call_duration=timedelta(hours=0,
                                                        minutes=10,
                                                        seconds=0),
                                call_price=1.26)
        CallDetail.objects.create(call_id=call,
                                  type_call=END,
                                  timestamp=before)

        call2 = Call.objects.create(source=phone,
                                    destination=phone2,
                                    call_id=71)

        BillCall.objects.create(call_id=call2,
                                call_start_date=before.date(),
                                call_start_time=time(10, 15, 20),
                                call_duration=timedelta(hours=35,
                                                        minutes=10,
                                                        seconds=25),
                                call_price=300.50)
        CallDetail.objects.create(call_id=call2,
                                  type_call=END,
                                  timestamp=before)

        call3 = Call.objects.create(source=phone2,
                                    destination=phone,
                                    call_id=72)
        BillCall.objects.create(call_id=call3,
                                call_start_date=now.date(),
                                call_start_time=time(10, 15, 20),
                                call_duration=timedelta(hours=35,
                                                        minutes=10,
                                                        seconds=25),
                                call_price=300.50)
        CallDetail.objects.create(call_id=call3,
                                  type_call=END,
                                  timestamp=now)

    def test_detail_url(self):
        with self.assertRaises(NoReverseMatch):
            reverse("bill:bill_detail_list")
        with self.assertRaises(NoReverseMatch):
            reverse("bill:bill_detail_list", kwargs={"source_number": "abc"})
        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31985853903"})
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_detail_items_now(self):
        now = timezone.now()
        before = now - relativedelta(months=1)
        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31985853903"})
        phone = Phone.objects.get(number="31985853903")
        data = {'id': phone.pk,
                'number': '31985853903',
                'period': before.strftime("%m/%Y"),
                'call_records':
                [{'call_id': 70,
                  'call_start_date': before.strftime("%Y-%m-%d"),
                  'call_start_time': '22:00:00',
                  'call_price': 'R$ 1,26',
                  'call_duration': '0h10m00s'},
                 {'call_id': 71,
                  'call_start_date': before.strftime("%Y-%m-%d"),
                  'call_start_time': '10:15:20',
                  'call_price': 'R$ 300,50',
                  'call_duration': '35h10m25s'}]
                }

        items = self.client.get(url).json()
        self.assertEqual(data, items)
        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31988888888"})
        items = self.client.get(url).json()
        self.assertEqual({}, items)

    def test_filter_month_year_get(self):
        now = timezone.now().date()
        now_str = now.strftime("%m/%Y")
        before = now - relativedelta(months=1)
        before_str = before.strftime("%m/%Y")

        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31985853903"})
        get_url = "%s?month_year=%s" % (url, before_str)
        items = self.client.get(get_url).json()
        phone = Phone.objects.get(number="31985853903")
        data = {'id': phone.pk,
                'number': '31985853903',
                'period': before_str,
                'call_records':
                [{'call_id': 70,
                  'call_start_date': before.strftime("%Y-%m-%d"),
                  'call_start_time': '22:00:00',
                  'call_price': 'R$ 1,26',
                  'call_duration': '0h10m00s'},
                 {'call_id': 71,
                  'call_start_date': before.strftime("%Y-%m-%d"),
                  'call_start_time': '10:15:20',
                  'call_price': 'R$ 300,50',
                  'call_duration': '35h10m25s'}]}
        self.assertEqual(data, items)

        get_url = "%s?month_year=%s" % (url, now_str)
        items = self.client.get(get_url).json()
        self.assertEqual({}, items)

    def test_date_error(self):
        url = reverse("bill:bill_detail_list", kwargs={"source_number":
                                                       "31985853903"})
        get_url = "%s?month_year=%s" % (url, "2015-01")
        items = self.client.get(get_url).json()
        self.assertEqual(["Date format is m/Y"], items)
        self.assertEqual(self.client.get(get_url).status_code, 400)
