# Generated by Django 3.2.9 on 2021-12-26 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corona', '0009_auto_20211226_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.ForeignKey(help_text='PCR 음성 필요 여부는 <태그>를 통해 작성해주시면 감사하겠습니다.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corona.restaurantcategory'),
        ),
    ]
