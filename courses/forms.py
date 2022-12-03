from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import *
from django.contrib.auth.models import User


class RegisterCourseForm(forms.ModelForm):
    feature = forms.BooleanField()

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterCourseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Course
        fields = ['title', 'description', 'duration',
                  'amount', 'cover_image', 'feature']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "groups")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.add(*self.cleaned_data['groups'])
            user.save()

        return user


class RegisterLessonForm(forms.ModelForm):
    feature = forms.BooleanField()

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterLessonForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Lesson
        fields = ['course', 'chapter_no', 'description',
                  'video', 'pdf']


class RegisterCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Category
        fields = ['name', 'image']
