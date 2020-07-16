# Generated by Django 3.0.2 on 2020-06-30 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0009_auto_20200622_0102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.University')),
            ],
        ),
    ]
