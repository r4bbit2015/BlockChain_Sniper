# Generated by Django 3.1.5 on 2021-02-18 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=0, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PriceMonitorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_times', models.DateTimeField(auto_now_add=True)),
                ('exchange_name', models.CharField(default=0, max_length=1024)),
                ('coin_name', models.CharField(default=0, max_length=1024)),
                ('current_price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('monitor_price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('monitor_statue', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MonitorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('get_times', models.DateTimeField(auto_now_add=True)),
                ('notice_data', models.CharField(default=0, max_length=1024)),
                ('notice_times', models.DateTimeField()),
                ('notice_coin_name', models.CharField(default=0, max_length=128)),
                ('exchange_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.exchangename')),
            ],
        ),
    ]
