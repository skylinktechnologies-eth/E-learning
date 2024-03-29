from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.


def only_int(value):
    if value.isdigit() == False:
        raise ValidationError('Phone Number contains characters')


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )
    security_question = models.CharField(
        _("Sequrity Question"), max_length=50, default="")
    security_answer = models.CharField(
        _("Sequrity Answer"), max_length=50, default="")
    birthday = models.DateField(
        _("Birthdate"), auto_now=False, auto_now_add=False)
    occupation = models.CharField(_("Occupation"), max_length=30)
    phone = models.CharField(blank=True, null=True,
                             max_length=15, validators=[only_int])

    def __str__(self) -> str:
        return self.user.username
