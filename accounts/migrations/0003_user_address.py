# Generated by Django 4.1 on 2022-10-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_city_user_education_user_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
