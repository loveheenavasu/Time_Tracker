from django.db import models

# Create your models here.

class CompanySocials(models.Model):
    twitter = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    youtube = models.CharField(max_length=100, null=True, blank=True)
    discord = models.CharField(max_length=100, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    pinterest = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    whatsapp = models.CharField(max_length=100, null=True, blank=True)


class CompanyDetails(models.Model):
    registered_name = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    contact = models.IntegerField()
    logo = models.CharField(max_length=100, null=True, blank=True)
    company_name_image = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100)
    address_directions = models.CharField(max_length=255, null=True, blank=True)
    theme_color = models.CharField(max_length=10, default='#8CC33F')
    social_accounts = models.ForeignKey(CompanySocials, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
