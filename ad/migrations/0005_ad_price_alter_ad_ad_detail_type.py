# Generated by Django 4.0.1 on 2022-01-21 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0004_rename_adobjecttype_addetailtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='price',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ad',
            name='ad_detail_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ads', to='ad.addetailtype'),
        ),
    ]