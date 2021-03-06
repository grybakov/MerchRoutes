# Generated by Django 2.0.4 on 2018-06-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mroute', '0005_auto_20180529_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routemodel',
            name='route_fri',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_fri_order',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_fri_status',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_mon',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_mon_order',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_mon_status',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_sat',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_sat_order',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_sat_status',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_sun',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_sun_order',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_sun_status',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_thu',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_thu_order',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_thu_status',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_tue',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_tue_order',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_tue_status',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_wed',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_wed_order',
        ),
        migrations.RemoveField(
            model_name='routemodel',
            name='route_wed_status',
        ),
        migrations.AddField(
            model_name='routemodel',
            name='route_rawArray',
            field=models.TextField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='routemodel',
            name='route_desc',
            field=models.TextField(max_length=500),
        ),
    ]
