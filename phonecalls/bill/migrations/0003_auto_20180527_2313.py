# Generated by Django 2.0.5 on 2018-05-27 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_auto_20180527_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billcall',
            name='call_start_date',
            field=models.DateField(),
        ),
    ]
