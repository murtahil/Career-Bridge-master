# Generated by Django 3.0.2 on 2020-06-22 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_auto_20200622_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.FileField(blank=True, default='logos\\defaultdp.jpg', null=True, upload_to='logos'),
        ),
    ]
