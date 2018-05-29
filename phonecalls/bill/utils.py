from bill.models import BillCall
from bill.bill_detail import BillDetail


def bill_create(call_id, start, end):
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
