# Generated by Django 3.0.2 on 2020-06-21 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20200620_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default='settings.MEDIA_ROOT/defaultdp.jpg', null=True, upload_to=''),
        ),
    ]
