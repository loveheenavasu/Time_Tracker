# Generated by Django 4.1 on 2022-10-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_projects_project_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
