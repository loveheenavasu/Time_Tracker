# Generated by Django 4.1 on 2022-10-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_projects_priority_alter_projects_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_category',
            field=models.CharField(choices=[('UI/UX Design', 'UI/UX Design'), ('Website Design', 'Website Design'), ('App Development', 'App Development'), ('Quality Assurance', 'Quality Assurance'), ('Development', 'Development'), ('Backend Development', 'Backend Development'), ('Software Testing', 'Software Testing'), ('Marketing', 'Marketing'), ('SEO', 'SEO'), ('Other', 'Other')], default='Other', max_length=255),
        ),
    ]