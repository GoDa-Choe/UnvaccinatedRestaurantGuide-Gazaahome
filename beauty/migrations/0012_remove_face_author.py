# Generated by Django 3.2 on 2021-11-22 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0011_alter_face_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='face',
            name='author',
        ),
    ]