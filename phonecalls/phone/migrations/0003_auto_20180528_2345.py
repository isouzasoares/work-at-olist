# Generated by Django 2.0.5 on 2018-05-28 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0002_auto_20180528_2258'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='calldetail',
            unique_together={('call_id', 'type_call')},
        ),
    ]