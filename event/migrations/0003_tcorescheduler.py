# Generated by Django 3.2 on 2021-12-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_scheduler'),
    ]

    operations = [
        migrations.CreateModel(
            name='TCoreScheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='T Scheduler status', max_length=30)),
                ('scheduler_code', models.CharField(max_length=30)),
                ('last_updated', models.CharField(max_length=50)),
            ],
        ),
    ]
