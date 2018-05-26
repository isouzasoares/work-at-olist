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

    def _get_total_days(self):
        return self.total_time.days

    def _get_total_seconds_charging_day(self):
        return self.end_interval_second - self.start_interval_second

    def calculate_bill_charging_time(self):
        start_time_seconds = self._get_interval_second(
            self.start_datetime.hour, self.start_datetime.minute,
            self.start_datetime.second)
        end_time_seconds = self._get_interval_second(
            self.end_datetime.hour, self.end_datetime.minute,
            self.end_datetime.second)

        if (start_time_seconds <= self.start_interval_second and
                end_time_seconds >= self.end_interval_second):
            second_start = self.start_interval_second
            second_end = self.end_interval_second

        if (start_time_seconds >= self.start_interval_second and
                end_time_seconds >= self.end_interval_second):
            second_start = start_time_seconds
            second_end = self.end_interval_second

        if (start_time_seconds <= self.start_interval_second and
                end_time_seconds <= self.end_interval_second):
            second_start = self.start_interval_second
            second_end = end_time_seconds

        if (start_time_seconds >= self.start_interval_second and
                end_time_seconds <= self.end_interval_second):
            second_start = start_time_seconds
            second_end = end_time_seconds

        total = second_end - second_start
        total += self._get_total_days() * (
            self.end_interval_second - self.start_interval_second)

        return total
