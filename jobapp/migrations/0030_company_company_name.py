# Generated by Django 3.2.16 on 2024-04-26 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0029_auto_20240426_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_name',
            field=models.CharField(default='Test Company', max_length=35),
            preserve_default=False,
        ),
    ]