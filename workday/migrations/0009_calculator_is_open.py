# Generated by Django 3.2 on 2021-08-11 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workday', '0008_alter_calculator_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculator',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
    ]
