# Generated by Django 4.1 on 2022-08-16 00:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_fund_chain_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]