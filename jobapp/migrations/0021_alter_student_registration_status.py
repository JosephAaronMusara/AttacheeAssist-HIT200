# Generated by Django 3.2.16 on 2024-04-12 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0020_alter_company_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_status',
            field=models.BooleanField(default=True),
        ),
    ]
