# Generated by Django 4.0.1 on 2022-01-21 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0005_ad_price_alter_ad_ad_detail_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(upload_to='AdImage/')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ad.ad')),
            ],
        ),
    ]