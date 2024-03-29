# Generated by Django 4.1.3 on 2023-01-01 08:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_event_course_trainer_alter_course_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='name',
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='sad', max_length=100, verbose_name='Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(default='23', max_length=100, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
