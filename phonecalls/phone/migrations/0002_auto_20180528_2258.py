# Generated by Django 2.0.5 on 2018-05-28 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.CharField(max_length=11),
        ),
    ]
