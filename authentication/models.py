from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

    birthday = models.DateField(
        _("Birthdate"), auto_now=False, auto_now_add=False)
    occupation = models.CharField(_("Occupation"), max_length=30)
    phone = PhoneNumberField(blank=True, null=True)
