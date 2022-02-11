# Generated by Django 4.0.1 on 2022-01-29 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0009_adcomments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Communications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='areadetail',
            old_name='area',
            new_name='total_area',
        ),
        migrations.AddField(
            model_name='areadetail',
            name='is_divisibility',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='areadetail',
            name='is_pledge',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='homedetail',
            name='building_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ad.buildingtype'),
        ),
        migrations.AlterField(
            model_name='homedetail',
            name='repair_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ad.repairtype'),
        ),
        migrations.CreateModel(
            name='ApartmentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers_room', models.IntegerField(blank=True, null=True)),
                ('total_area', models.IntegerField(blank=True, null=True)),
                ('floor', models.IntegerField(blank=True, null=True)),
                ('total_floor', models.IntegerField(blank=True, null=True)),
                ('year_construction', models.IntegerField(blank=True, null=True)),
                ('building_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ad.buildingtype')),
                ('repair_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ad.repairtype')),
            ],
        ),
        migrations.AddField(
            model_name='areadetail',
            name='communications',
            field=models.ManyToManyField(blank=True, to='ad.Communications'),
        ),
    ]