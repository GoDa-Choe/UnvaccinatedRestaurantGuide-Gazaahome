# Generated by Django 3.2 on 2021-07-18 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workday', '0008_alter_calculator_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('barracks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarracksComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('barracks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barracks.barracks')),
                ('calculator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workday.calculator')),
            ],
        ),
    ]
