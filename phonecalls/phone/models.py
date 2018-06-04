from django.db import models
from django.db.models.signals import post_save

from phone.choices import TYPE_CALL_CHOICES
from bill.utils import bill_create

# Create your models here.


class Phone(models.Model):
    number = models.CharField(max_length=11)


class Call(models.Model):
    call_id = models.AutoField(primary_key=True)
    source = models.ForeignKey(Phone, related_name="source",
                               on_delete=models.PROTECT)
    destination = models.ForeignKey(Phone, related_name="destination",
                                    on_delete=models.PROTECT)


class CallDetail(models.Model):
    call_id = models.ForeignKey(Call, on_delete=models.PROTECT)
    type_call = models.CharField(max_length=10, choices=TYPE_CALL_CHOICES)
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ("call_id", "type_call")


def save_price(sender, instance, **kwargs):
    """The function execute after
    save registry in model CallDetail

    .. note::
            If call detail count == 2, the system calculate and
            create billdetail values
    """
    call_detail = instance.call_id.calldetail_set.all()
    if call_detail.count() == 2:
        start, end = call_detail
        bill_create(instance.call_id, start.timestamp, end.timestamp)

post_save.connect(save_price, sender=CallDetail)
