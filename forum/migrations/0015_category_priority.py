# Generated by Django 3.2 on 2021-07-25 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0014_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='priority',
            field=models.IntegerField(default=1),
        ),
    ]
