# Generated by Django 3.2 on 2021-12-27 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Scheduler status', max_length=30)),
                ('last_started', models.CharField(max_length=50)),
            ],
        ),
    ]
