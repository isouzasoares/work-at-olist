from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from phone.models import Phone, Call, CallDetail
from phone.choices import START, END


class CallModelTest(TestCase):

    def setUp(self):
        phone = Phone.objects.create(number="31985853903")
        phone2 = Phone.objects.create(number="31985853901")
        Call.objects.create(source=phone,
                            destination=phone2,
                            call_id=70)

    def test_call_detail_add(self):
        call = Call.objects.get(call_id=70)
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

        with self.assertRaises(IntegrityError):
            CallDetail.objects.create(call_id=call,
                                      type_call=START,
                                      timestamp=end)
