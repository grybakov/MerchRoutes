# Generated by Django 2.0.4 on 2018-07-06 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mroute', '0010_auto_20180706_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='netmodel',
            name='net_icon_link',
            field=models.CharField(max_length=300, null=True, verbose_name='Ссылка на иконку'),
        ),
        migrations.AlterField(
            model_name='netmodel',
            name='net_icon_size',
            field=models.CharField(max_length=10, null=True, verbose_name='Размеры иконки (через запятую: X, Y)'),
        ),
    ]