# Generated by Django 3.0.2 on 2020-06-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('project_description', models.TextField()),
                ('develop_by', models.CharField(max_length=100)),
                ('develop_for', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('bidding_start', models.DateTimeField(auto_now_add=True)),
                ('bidding_end', models.DateTimeField()),
            ],
        ),
    ]
