# Generated by Django 4.0.1 on 2022-02-06 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0014_adlike_isliked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentdetail',
            name='total_area',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homedetail',
            name='total_area',
            field=models.FloatField(blank=True, null=True),
        ),
    ]