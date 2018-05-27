from decimal import Decimal
from datetime import datetime, time

from django.test import SimpleTestCase

from bill.bill_detail import BillDetail


class BillDetailTestCase(SimpleTestCase):

    def test_instance_object(self):
        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 25, 10, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(isinstance(detail, BillDetail), True)
        self.assertEqual(detail.total_hour, 133200.0)

    def test_instance_error(self):
        now = datetime(2017, 5, 25, 0, 0, 0)
        after = datetime(2017, 5, 23, 0, 0, 0)
        self.assertRaises(ValueError, BillDetail, now, after)

    def test_time_second(self):
        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 25, 10, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail._get_interval_second(22), 79200.0)

    def test_total_day(self):
        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 25, 10, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail._get_total_days_automatic_calculate(), 1)

    def test_total_seconds_charging_day(self):
        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 25, 10, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail._get_total_seconds_charging_day(),
                         79200.0 - 21600.0)

    def test_calculate_bill_charging_time(self):
        now = datetime(2017, 5, 23, 10, 00, 00)
        after = datetime(2017, 5, 23, 20, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 36000)

        now = datetime(2017, 5, 23, 5, 00, 00)
        after = datetime(2017, 5, 23, 7, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 3600)

        now = datetime(2017, 5, 23, 21, 00, 00)
        after = datetime(2017, 5, 23, 23, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 3600)

        now = datetime(2017, 5, 23, 5, 00, 00)
        after = datetime(2017, 5, 23, 23, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 57600)

        now = datetime(2017, 5, 23, 4, 00, 00)
        after = datetime(2017, 5, 23, 5, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 0)

        now = datetime(2017, 5, 23, 23, 00, 00)
        after = datetime(2017, 5, 23, 23, 10, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 0)

        now = datetime(2017, 5, 23, 21, 00, 00)
        after = datetime(2017, 5, 24, 5, 10, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 3600)

        now = datetime(2017, 5, 23, 21, 00, 00)
        after = datetime(2017, 5, 25, 7, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 64800)

        now = datetime(2017, 5, 23, 0, 0, 0)
        after = datetime(2017, 5, 24, 0, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 57600)

        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 25, 21, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 115200)

        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 27, 21, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 230400)

        now = datetime(2017, 5, 23, 7, 00, 00)
        after = datetime(2017, 5, 24, 7, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.calculate_bill_charging_time(), 57600)

    def test_get_total_time_call(self):
        now = datetime(2017, 5, 23, 7, 00, 00)
        after = datetime(2017, 5, 24, 7, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_time_call(), "24h00m00s")

        now = datetime(2017, 5, 23, 7, 00, 00)
        after = datetime(2017, 5, 23, 8, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_time_call(), "1h00m00s")

        now = datetime(2017, 5, 23, 7, 00, 00)
        after = datetime(2017, 5, 23, 7, 10, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_time_call(), "0h10m00s")

        now = datetime(2017, 5, 23, 7, 00, 00)
        after = datetime(2017, 5, 23, 7, 00, 30)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_time_call(), "0h00m30s")

    def test_get_total_price_call(self):
        now = datetime(2017, 5, 23, 10, 00, 00)
        after = datetime(2017, 5, 23, 20, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_price_call(), Decimal('54.36'))

        now = datetime(2017, 5, 23, 4, 00, 00)
        after = datetime(2017, 5, 23, 5, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_price_call(), Decimal('0.36'))

        now = datetime(2017, 5, 23, 23, 00, 00)
        after = datetime(2017, 5, 23, 23, 10, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_price_call(), Decimal('0.36'))

        now = datetime(2017, 5, 23, 6, 00, 00)
        after = datetime(2017, 5, 23, 6, 00, 50)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_price_call(), Decimal('0.36'))

        now = datetime(2017, 5, 23, 6, 00, 00)
        after = datetime(2017, 5, 23, 6, 10, 10)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_price_call(), Decimal('1.26'))

        now = datetime(2017, 5, 23, 7, 00, 00)
        after = datetime(2017, 5, 24, 7, 00, 00)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_price_call(),
                         Decimal('86.76'))

        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 25, 21, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_total_price_call(),
                         Decimal('173.16'))

    def test_get_start_time(self):
        now = datetime(2017, 5, 23, 21, 0, 0)
        after = datetime(2017, 5, 25, 21, 0, 0)
        detail = BillDetail(now, after)
        self.assertEqual(detail.get_start_time(),
                         time(21, 0))
