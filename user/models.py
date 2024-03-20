from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
import random

import os
from uuid import uuid4
# Create your models here.



class UserManager(BaseUserManager):
    def create_user(self, phone,email,first_name,last_name=None,referrer=None ,password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('user must have a phone number')
        if not email:
            raise ValueError('user must have a email')

        if not password:
            raise ValueError('user must have a password')
        user_obj = self.model(
            email=self.normalize_email(email),
            phone=phone,
            last_name=last_name,
            first_name=first_name,
            referrer=referrer
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    def create_main_user(self, email, password=None, is_staff=True, is_active=True, is_admin=True):
        if not email:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            email=email
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self, phone,email,name=None,username=None, password=None, is_staff=True, is_active=True, is_admin=True):
        if not phone:
            raise ValueError('user must have a phone number')
        if not email:
            raise ValueError('user must have a email')

        if not password:
            raise ValueError('user must have a password')
        user_obj = self.model(
            email=self.normalize_email(email),
            phone=phone,
            username=username,
            name=name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password=None):
        user = self.create_main_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user

def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )
         

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class User(AbstractBaseUser):
    phone_regex      = RegexValidator( regex=r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone            = models.CharField(validators=[phone_regex], max_length=17)
    first_name             = models.CharField(max_length = 20, blank = True, null = True)
    tag             = models.CharField(max_length = 20, blank = True, null = True)
    last_name         = models.CharField(max_length = 80, blank = True, null = True)
    country_origin         = models.CharField(max_length = 80, blank = True, null = True)
    join_reason         = models.CharField(max_length = 180, blank = True, null = True)
    recoveryCode     = models.CharField(max_length = 10, blank = True, null = True)
    avatar               =   models.ImageField(upload_to = 'profileImage/', default=None, null = True, blank = True)
    email            = models.EmailField(unique=True)
    
    transaction_pin = models.IntegerField(blank=True,null=True)
    passcode         = models.IntegerField(blank=True,null=True)
    first_login      = models.BooleanField(default=False)
    verified      = models.BooleanField(default=False,blank=True,null=True)
    active           = models.BooleanField(default=True)
    staff            = models.BooleanField(default=False)
    admin            = models.BooleanField(default=False)
    timestamp        = models.DateTimeField(auto_now_add=True)
    create_at       =   models.DateTimeField(default=timezone.now)
    is_bvn          = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referral_link = models.URLField(blank=True, null=True)
    number_of_referral = models.IntegerField(default=0)
    point = models.IntegerField(blank=True,null=True,default=0)
    referrer = models.CharField(max_length=10, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.first_name
    def get_email(self):
        return self.email
    def get_tag(self):
        labTag = self.tag + "@LabTag"
        return labTag
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True



    # Override the save method
    def save(self, *args, **kwargs):
        # Generate referral code and referral link if not already set
        if not self.referral_code:
            self.referral_code = str(uuid4())[:8]  # Generate a unique referral code


        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class EmailVerifyTable(models.Model):
    email = models.CharField(("email"), max_length=50)
    is_verified = models.CharField(("isVerified"), max_length=50, default=False)
    code = models.CharField(("code"), max_length=50,null=True,blank=True)

class PhoneVerifyTable(models.Model):
    phone = models.CharField(("phone"), max_length=50)
    is_verified = models.CharField(("isVerified"), max_length=50, default=False)
    code = models.CharField(("code"), max_length=50,null=True,blank=True)

class bvnVerifyTable(models.Model):
    bvn = models.CharField(("bvn"), max_length=50)
    is_verified = models.CharField(("isVerified"), max_length=50, default=False)

