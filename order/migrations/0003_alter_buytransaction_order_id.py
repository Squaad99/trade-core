# Generated by Django 3.2 on 2021-12-30 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_dummy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buytransaction',
            name='order_id',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]