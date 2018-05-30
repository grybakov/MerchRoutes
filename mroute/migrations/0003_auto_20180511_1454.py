# Generated by Django 2.0.4 on 2018-05-11 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mroute', '0002_auto_20180404_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metromodel',
            name='metro_name_en',
        ),
        migrations.AlterField(
            model_name='marketmodel',
            name='market_address_en',
            field=models.CharField(max_length=400, verbose_name='Адрес (латиница)'),
        ),
        migrations.AlterField(
            model_name='marketmodel',
            name='market_address_ru',
            field=models.CharField(max_length=400, verbose_name='Адрес (кирилица)'),
        ),
        migrations.AlterField(
            model_name='marketmodel',
            name='market_is_active',
            field=models.BooleanField(default=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='marketmodel',
            name='market_lat',
            field=models.FloatField(verbose_name='Координата X'),
        ),
        migrations.AlterField(
            model_name='marketmodel',
            name='market_lng',
            field=models.FloatField(verbose_name='Координата Y'),
        ),
        migrations.AlterField(
            model_name='marketmodel',
            name='market_net',
            field=models.CharField(choices=[('DKS', 'Дикси'), ('PRKRS', 'Перекресток'), ('VKTR', 'Виктория'), ('BLL', 'BILLA'), ('KRS', 'Карусель')], max_length=400, verbose_name='Сеть'),
        ),
    ]
