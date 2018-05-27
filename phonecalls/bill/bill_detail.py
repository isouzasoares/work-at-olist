from datetime import datetime, date, time


class BillDetail(object):

    def __init__(self, start_datetime, end_datetime,
                 start_value=0.36, call_value=0.09,
                 start_interval_hour=6, end_interval_hour=22):

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
        timeobj = time(hour, minutes, seconds)
        seconds = datetime.combine(date.min, timeobj) - datetime.min
        seconds = seconds.total_seconds()
        return seconds

    def _get_total_days_automatic_calculate(self):
        total_day = (self.end_datetime - self.start_datetime).days

        if total_day > 1:
            start_day = self.start_datetime.replace(
                day=self.start_datetime.day, hour=23, minute=59, second=59)
            end_day = self.end_datetime.replace(
                day=self.end_datetime.day - 1, hour=23, minute=59, second=59)
            return (end_day - start_day).days

        return total_day

    def _get_total_seconds_charging_day(self):
        return self.end_interval_second - self.start_interval_second

    def calculate_bill_charging_day(self, start_datetime, end_datetime):
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

        if self._get_total_days_automatic_calculate():
            start_date_day = self.start_datetime.replace(
                day=self.start_datetime.day, hour=23, minute=59, second=59)

            end_date_day = self.end_datetime.replace(
                day=self.end_datetime.day, hour=0, minute=0, second=0)

            second_start = self.calculate_bill_charging_day(
                self.start_datetime, start_date_day)

            second_end = self.calculate_bill_charging_day(
                end_date_day, self.end_datetime)

            total = second_end + second_start

            date_validate = (
                self.start_datetime.date() !=
                self.end_datetime.replace(
                    day=self.end_datetime.day - 1).date())

            if self.end_datetime > end_date_day and date_validate:
                total += self._get_total_days_automatic_calculate() * (
                    self.end_interval_second - self.start_interval_second)
            return total
        else:
            return self.calculate_bill_charging_day(self.start_datetime,
                                                    self.end_datetime)
