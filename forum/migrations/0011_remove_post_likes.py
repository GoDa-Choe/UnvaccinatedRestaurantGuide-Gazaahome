# Generated by Django 3.2 on 2021-05-14 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
