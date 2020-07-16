# Generated by Django 3.0.2 on 2020-06-19 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
        ('company', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='develop_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.University'),
        ),
        migrations.AlterField(
            model_name='project',
            name='develop_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
    ]
