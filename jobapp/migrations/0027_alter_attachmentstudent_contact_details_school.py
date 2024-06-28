# Generated by Django 3.2.16 on 2024-04-21 20:41

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0026_attachmentstudent_has_school_supervisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentstudent',
            name='contact_details_school',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default='', max_length=128, region=None),
        ),
    ]