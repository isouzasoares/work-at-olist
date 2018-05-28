from django.db import models

from phone.models import Call

# Create your models here.


class BillCall(models.Model):
    call = models.ForeignKey(Call, on_delete=models.PROTECT)
    call_start_date = models.DateField()
    call_start_time = models.TimeField()
    call_duration = models.DurationField()
    call_price = models.DecimalField(max_digits=10, decimal_places=2)
