from django.db import models
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Course(models.Model):
    category = models.ForeignKey(
        "courses.Category", verbose_name=_("Course Category"), on_delete=models.CASCADE)
    title = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    duration = models.DurationField(_("Course Duration"))
    amount = models.DecimalField(_("Price"),  decimal_places=2, max_digits=10)
    cover_image = models.ImageField(
        _("Cover Image"), null=True, upload_to="image/", blank=True)
    feature = models.BooleanField(_("Courese type"))
    trainer = models.ForeignKey(
        settings.AUTH_USER,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

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
    course = models.ForeignKey("courses.Course", verbose_name=_(
        "Course"), on_delete=models.CASCADE, null=False, blank=False)


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=30)
    image = models.ImageField(
        _("Category Image"), upload_to="image/", null=True, blank=True)

    def __str__(self):
        return self.name


class Attending(models.Model):
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)
    payment = models.OneToOneField('courses.Payment', verbose_name=_(
        "Payment"), on_delete=models.PROTECT)


class Payment(models.Model):
    payment_date = models.DateTimeField(default=timezone.now, )
    transaction_id = models.CharField(_("Transaction Id"), max_length=100)
    bank_reference_number = models.CharField(
        _("Bank Reference Number"), max_length=50)
    bank_name = models.CharField(
        _("Bank Name"), max_length=50)
    student = models.ForeignKey(
        'authentication.Student', verbose_name=_("Student"), on_delete=models.PROTECT)
    course_order_id = models.ForeignKey(
        "courses.Course", verbose_name=_("Course"), on_delete=models.CASCADE)
    status = models.BooleanField(_("Status"), default=False)


class TrainerCourse(models.Model):
    trainer = models.ForeignKey(
        settings.AUTH_USER,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        "courses.Course", verbose_name="Course", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
