# Generated by Django 4.0.1 on 2022-02-13 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_notifcationtype_rating_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifcationtype',
            options={'verbose_name': 'Тип уведемлений', 'verbose_name_plural': 'Типы уведемлений'},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Уведемление', 'verbose_name_plural': 'Уведемлений'},
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Рейтинг', 'verbose_name_plural': 'Рейтинги'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользаватель', 'verbose_name_plural': 'Пользаватели'},
        ),
        migrations.AlterModelOptions(
            name='usertype',
            options={'verbose_name': 'Тип пользавателей', 'verbose_name_plural': 'Типы пользователей'},
        ),
    ]