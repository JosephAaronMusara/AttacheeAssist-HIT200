# Generated by Django 3.2.16 on 2024-04-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0023_auto_20240421_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentstudent',
            name='first_visit_details',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='attachmentstudent',
            name='second_visit_details',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='attachmentstudent',
            name='supervisor_from_school',
            field=models.CharField(default='', max_length=100),
        ),
    ]
