from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from phone.models import Phone, Call, CallDetail
from phone.choices import START, END
from bill.utils import bill_create, get_month_year


class CallModelTest(TestCase):

    def setUp(self):
        phone = Phone.objects.create(number="31985853903")
        phone2 = Phone.objects.create(number="31985853901")
        Call.objects.create(source=phone,
                            destination=phone2,
                            call_id=70)
        Call.objects.create(source=phone,
                            destination=phone2,
                            call_id=71)

    def test_bill_call_create(self):
        call = Call.objects.get(call_id=70)
        start = timezone.datetime(2017, 5, 23, 21, 57, 13,
                                  tzinfo=timezone.get_current_timezone())
        end = timezone.datetime(2017, 5, 23, 22, 00, 00,
                                tzinfo=timezone.get_current_timezone())
        bill = bill_create(call, start, end)
        self.assertEqual(bill.call_id, call)

    def test_call_detail_add(self):
        call = Call.objects.get(call_id=71)
        start = timezone.datetime(2017, 5, 23, 21, 57, 13,
                                  tzinfo=timezone.get_current_timezone())
        CallDetail.objects.create(call_id=call,
                                  type_call=START,
                                  timestamp=start)
        self.assertEqual(CallDetail.objects.count(), 1)
        end = timezone.datetime(2017, 5, 23, 22, 00, 00,
                                tzinfo=timezone.get_current_timezone())
        CallDetail.objects.create(call_id=call,
                                  type_call=END,
                                  timestamp=end)
        self.assertEqual(CallDetail.objects.count(), 2)
        self.assertEqual(end.date(), call.billcall.call_start_date)
        self.assertEqual(Decimal("0.54"), call.billcall.call_price)

        with self.assertRaises(IntegrityError):
            CallDetail.objects.create(call_id=call,
                                      type_call=START,
                                      timestamp=end)

    def test_util_month_year(self):
        now = timezone.now()
        month_year = now - relativedelta(months=1)
        month_year = month_year.replace(day=1)
        self.assertEqual(get_month_year(), month_year.date())

        now = timezone.datetime(2018, 5, 1).date()
        self.assertEqual(get_month_year("05/2018"), now)

        self.assertRaises(ValueError, get_month_year, "05-2018")
