# Generated by Django 4.0.1 on 2022-02-06 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0015_alter_apartmentdetail_total_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areadetail',
            name='total_area',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
