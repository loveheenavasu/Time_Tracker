from pyexpat import model
from typing import ChainMap
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, )
from django.db import models
from departments.models import Departments
from django.conf import settings

# from questions.models import User, Subject





class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str = None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str = None, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self._create_user(email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, null=True, blank=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(default='avatar.jpg', upload_to='profile_pics')
    email = models.EmailField('email address', max_length=255, unique=True, error_messages={'unique': "A user with that email already exists.", })
    contact = models.BigIntegerField(null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    City = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=1000, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField('admin',default=True,help_text=('Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'), )
    is_active = models.BooleanField('active',default=True,help_text=('Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'),)
    is_staff = models.BooleanField('staff status',default=False,help_text='Designates whether the user can log into this admin site.',)
    is_projectmanager = models.BooleanField('project manager status', default=False,help_text='Designates whether the user can log into this admin site.', )
    is_employee = models.BooleanField(default=False)
    is_TeamLeader = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_user_id(self):
        return self.id


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebooklink = models.CharField(max_length=1000, null=True, blank=True)
    instagramlink = models.CharField(max_length=1000, null=True, blank=True)
    linkedinlink = models.CharField(max_length=1000, null=True, blank=True)
    githublink = models.CharField(max_length=1000, null=True, blank=True)
    websitelink = models.CharField(max_length=1000, null=True, blank=True)




  







