# Generated by Django 3.2.9 on 2021-12-30 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corona', '0002_restaurant_content2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='content2',
        ),
    ]
