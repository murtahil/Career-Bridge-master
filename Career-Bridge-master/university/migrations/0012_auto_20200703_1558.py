# Generated by Django 3.0.2 on 2020-07-03 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0011_bidding_revisions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='ranking',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
