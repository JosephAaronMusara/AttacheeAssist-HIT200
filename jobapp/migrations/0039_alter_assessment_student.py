# Generated by Django 3.2.16 on 2024-04-28 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0038_alter_assessment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.attachmentstudent'),
        ),
    ]