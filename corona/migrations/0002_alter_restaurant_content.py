# Generated by Django 3.2.9 on 2021-12-30 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corona', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
