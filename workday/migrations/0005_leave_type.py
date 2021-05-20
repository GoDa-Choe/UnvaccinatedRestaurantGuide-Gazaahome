# Generated by Django 3.2 on 2021-05-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workday', '0004_dayoff'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='type',
            field=models.CharField(choices=[('ye', '연가'), ('po', '포상'), ('wi', '위로'), ('bo', '보상'), ('ch', '청원'), ('tp', '예정')], default='ye', max_length=2),
            preserve_default=False,
        ),
    ]
