from decimal import Decimal
from datetime import datetime, date, time


class BillDetail:
    """The object identifies the intersection of the
    collection intervals and calculates their due values
    """

    def __init__(self, start_datetime, end_datetime,
                 start_value=0.36, call_value=0.09,
                 start_interval_hour=6, end_interval_hour=22):
        """Initiates BillDetail
        :param start_datetime: The start datetime period
        :type start_datetime: datetime

        :param end_datetime: the end datetime period
        :type currency: datetime

        :param start_value: The value standing charge
        :type: float

        :param call_value: The value fractioned charge
        :type: float

        :param start_interval_hour: Starts interval hour for standart time call
        :type: int

        :param end_interval_hour: Ends interval hour for standart time call
        :type: int
        """

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

        if self.end_datetime < self.start_datetime:
            raise ValueError("end_datetime is < start_datetime")

        self.total_time = end_datetime - start_datetime
        self.total_hour = self.total_time.total_seconds()
        self.start_value = start_value
        self.call_value = call_value
        self.start_interval_second = self._get_interval_second(
            start_interval_hour)
        self.end_interval_second = self._get_interval_second(
            end_interval_hour)

    def _get_interval_second(self, hour, minutes=0, seconds=0):
        """Convert hour, minutes, seconds to total seconds.
        :param hour: hour for conversion
        :type: int

        :param minutes: minutes for conversion
        :type: int

        :param seconds: seconds for conversion
        :type: int

        :returns: total seconds, float
        """
        timeobj = time(hour, minutes, seconds)
        seconds = datetime.combine(date.min, timeobj) - datetime.min
        seconds = seconds.total_seconds()
        return seconds

    def _get_total_days_automatic_calculate(self):
        """Calculates total of whole days for multiplicated automatic interval

        .. note::
            The method not include start day and ends day, case total day is >
            1.

        :returns: total days, int
        """
        total_day = (self.end_datetime - self.start_datetime).days

        if total_day > 1:
            start_day = self.start_datetime.replace(
                day=self.start_datetime.day, hour=23, minute=59, second=59)
            end_day = self.end_datetime.replace(
                day=self.end_datetime.day - 1, hour=23, minute=59, second=59)
            return (end_day - start_day).days

        return total_day

    def _get_total_seconds_charging_day(self):
        """Calculates total seconds for interval starts and end

        :returns: total seconds, float
        """
        return self.end_interval_second - self.start_interval_second

    def _calculate_bill_charging_day(self, start_datetime, end_datetime):
        """Calculates total seconds intersects for start_datetime and end_datetime and
        interval start and interval end

        :param start_datetime: start_datetime period
        :type: datetime

        :param seconds: end_datetime period
        :type: datetime

        .. note::
            each one "if" represents a possibility of intersection

        :return float
        """
        total = 0
        start_time_seconds = self._get_interval_second(
            start_datetime.hour, start_datetime.minute,
            start_datetime.second)
        end_time_seconds = self._get_interval_second(
            end_datetime.hour, end_datetime.minute,
            end_datetime.second)

        if (self.start_interval_second <= start_time_seconds <=
                end_time_seconds <= self.end_interval_second):
            total = end_time_seconds - start_time_seconds

        elif (start_time_seconds <= self.start_interval_second <=
                end_time_seconds <= self.end_interval_second):
            total = end_time_seconds - self.start_interval_second

        elif (self.start_interval_second <= start_time_seconds <=
                self.end_interval_second <= end_time_seconds):
            total = self.end_interval_second - start_time_seconds

        elif (self.start_interval_second <= start_time_seconds <=
                self.end_interval_second >= end_time_seconds):
            total = self.end_interval_second - start_time_seconds

        elif (self.start_interval_second >= start_time_seconds <=
                end_time_seconds >= self.end_interval_second):
            total = self.end_interval_second - self.start_interval_second

        return total

    def calculate_bill_charging_time(self):
        """Calculates total bill charging time

        .. note::
            If total of days > 1, the method calculates the parts bill charging
            for start day and ends day, multiply after the days complete with
            the intervals passed

        :return float
        """

        if self._get_total_days_automatic_calculate():
            start_date_day = self.start_datetime.replace(
                day=self.start_datetime.day, hour=23, minute=59, second=59)

            end_date_day = self.end_datetime.replace(
                day=self.end_datetime.day, hour=0, minute=0, second=0)

            second_start = self._calculate_bill_charging_day(
                self.start_datetime, start_date_day)

            second_end = self._calculate_bill_charging_day(
                end_date_day, self.end_datetime)

            total = second_end + second_start

            date_validate = (
                self.start_datetime.date() !=
                self.end_datetime.replace(
                    day=self.end_datetime.day - 1).date())

            if date_validate:
                total += self._get_total_days_automatic_calculate() * (
                    self.end_interval_second - self.start_interval_second)
            return total
        else:
            return self._calculate_bill_charging_day(self.start_datetime,
                                                     self.end_datetime)

    def get_total_time_call(self):
        """Returns total time for end_datetime - start_datetime

        :return timedelta object
        """
        return self.total_time

    def get_start_time(self):
        """Returns total starts hour, minutes and seconds

        :return time object
        """
        return time(self.start_datetime.hour,
                    self.start_datetime.minute,
                    self.start_datetime.second)

    def get_total_price_call(self):
        """Returns total price for call

        .. note::
            The call price is start_value + total seconds interval * call_value

        :return decimal object
        """
        total = Decimal(str(self.start_value))
        time_total = self.calculate_bill_charging_time() // 60
        total += Decimal(str(time_total)) * Decimal(str(self.call_value))
        return Decimal(str(total)).normalize()
