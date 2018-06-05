from dateutil.relativedelta import relativedelta
from django.utils import timezone

from bill.models import BillCall
from bill.bill_detail import BillDetail


def bill_create(call_id, start, end):
    """Get or create the BillDetail registry

    :param call_id: call model object
    :type call_id: call object

    :param start: the end datetime period
    :type currency: datetime

    :param end: The value standing charge
    :type: datetime

    .. note::
        The function calculate the call detail 'BillDetail'
        and saves in model BillCall

    :returns: billdetail object

    """
    bill_detail_obj = getattr(call_id.call_id, "billcall", False)
    bill_detail = BillDetail(start, end)

    if bill_detail_obj:
        bill_obj = bill_detail_obj
    else:
        bill_obj = BillCall()

    bill_obj.call_id = call_id
    bill_obj.call_start_date = start.date()
    bill_obj.call_start_time = bill_detail.get_start_time()
    bill_obj.call_duration = bill_detail.get_total_time_call()
    bill_obj.call_price = bill_detail.get_total_price_call()
    bill_obj.save()
    return bill_obj


def get_month_year(month_year):
    now = timezone.now().replace(day=1).date()
    if not month_year:
        month_year = now - relativedelta(months=1)
    else:
        try:
            month_year = timezone.datetime.strptime(month_year, "%m/%Y")
            month_year = month_year.date()
        except:
            raise ValueError

    month_year = month_year.replace(day=1)

    if month_year < now:
        return month_year

    return None
