# Generated by Django 3.2 on 2021-12-31 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_buytransaction_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='buytransaction',
            name='test_mode',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='test_mode',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='selltransaction',
            name='test_mode',
            field=models.BooleanField(default=True),
        ),
    ]
