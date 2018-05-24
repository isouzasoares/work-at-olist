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

    def _get_interval_second(self, time_hour):
        timeobj = time(time_hour, 0)
        seconds = datetime.combine(date.min, timeobj) - datetime.min
        seconds = seconds.total_seconds()
        return seconds

    def _get_total_days(self):
        return self.total_time.days
