from django.db import models

from .choices import TYPE_CALL_CHOICES

# Create your models here.


class Phone(models.Model):
    number = models.CharField(max_length=9)


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
