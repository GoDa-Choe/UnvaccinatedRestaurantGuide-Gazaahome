# Generated by Django 3.2 on 2021-07-18 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('barracks', '0003_rename_barrackscomment_guestbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='barracks',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='barracks.barracks'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
