from django.db import models
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Course(models.Model):
    title = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    duration = models.DurationField(_("Course Duration"))
    amount = models.DecimalField(_("Price"),  decimal_places=2, max_digits=10)
    cover_image = models.ImageField(
        _("Room Image"), null=True, upload_to="image/", blank=True)
    feature = models.BooleanField(_("Courese type"))

    def __str__(self):
        return self.title


class Lesson(models.Model):
    chapter_no = models.IntegerField(_("Chapter No"))
    description = models.TextField(_("Objectives of the Lesson"))
    video = models.FileField(
        _("Lesson Video"), upload_to="video/", null=True, blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    pdf = models.FileField(
        _("Lesson Pdf"), upload_to="file/", null=True, blank=True)

    feature = models.BooleanField(_("lesson Type"), default=True)


class Attending(models.Model):
    date = models.DateField(default=timezone.now)
    course = models.ForeignKey("courses.Course", verbose_name=_(
        "Building"), on_delete=models.PROTECT)
    student = models.ForeignKey(
        'authentication.Student', verbose_name=_("Student"), on_delete=models.PROTECT)


class Category(models.Model):
    name = models.CharField(_("Course Category"), max_length=30)
    image = models.ImageField(
        _("Category Image"), upload_to="image/", null=True, blank=True)
