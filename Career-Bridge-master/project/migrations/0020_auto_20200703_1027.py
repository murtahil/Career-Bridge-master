# Generated by Django 3.0.2 on 2020-07-03 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
