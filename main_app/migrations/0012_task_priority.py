# Generated by Django 4.1 on 2022-10-10 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_task_task_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('HIGHEST', 'Highest'), ('LOWEST', 'Lowest'), ('MEDIUM', 'Medium')], default='Lowest', max_length=255),
        ),
    ]