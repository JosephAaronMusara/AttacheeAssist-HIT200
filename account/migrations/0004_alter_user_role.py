# Generated by Django 3.2.16 on 2024-04-26 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('employer', 'Employer'), ('employee', 'Employee'), ('coordinator', 'Coordinator'), ('supervisor', 'Supervisor'), ('worksupervisor', 'Worksupervisor')], max_length=15),
        ),
    ]