# Generated by Django 4.0.1 on 2022-02-20 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0018_areadetail_unit_of_measure'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='views',
            field=models.BigIntegerField(default=0),
        ),
    ]
