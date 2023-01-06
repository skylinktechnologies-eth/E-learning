from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class RegisterCourseForm(forms.ModelForm):
    feature = forms.BooleanField()

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterCourseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Course
        fields = ['category', 'title', 'description', 'duration',
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


class RegisterPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super(RegisterPaymentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payment
        fields = ['course_order_id', 'bank_name',
                  'transaction_id', 'bank_reference_number', ]


class RegisterCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Category
        fields = ['name', 'image']


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "password1", "password2")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.groups.add()
            user.save()

        return user


class TrainerRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "password1", "password2")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            group = Group.objects.get(name='trainer')
            group.user_set.add(user)
            # user.groups.add('trainer')
            group.save()
            user.save()

        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class eventRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(eventRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date']
        widget = {'start_date': DateInput(), 'end_date': DateInput()}
