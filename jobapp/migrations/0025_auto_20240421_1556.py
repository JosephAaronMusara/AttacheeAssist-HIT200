# Generated by Django 3.2.16 on 2024-04-21 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0024_auto_20240421_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentstudent',
            name='first_visit_details',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='attachmentstudent',
            name='second_visit_details',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='attachmentstudent',
            name='supervisor_from_school',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]