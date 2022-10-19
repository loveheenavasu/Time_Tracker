# Generated by Django 4.1 on 2022-10-18 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_projects_icons'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectIcons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='projects',
            name='icons',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.projecticons'),
        ),
    ]
