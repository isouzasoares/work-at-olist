from django.db import models


class BillCall(models.Model):
    call_id = models.OneToOneField("phone.Call", on_delete=models.PROTECT)
    call_start_date = models.DateField()
    call_start_time = models.TimeField()
    call_duration = models.DurationField()
    call_price = models.DecimalField(max_digits=10, decimal_places=2)
