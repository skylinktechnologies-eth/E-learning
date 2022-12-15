from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "birthday",
            "occupation",
            "phone",
            "security_question",
            "security_answer",
        ]


class UserRegistrationForm(UserCreationForm):
    occupation = forms.CharField(
        label="Occupation", max_length=100, required=False)
    birthday = forms.DateTimeField(label="BirthDate", widget=DateInput)

    security_question = forms.CharField(
        label="Security Question", max_length=100, required=False)
    security_answer = forms.CharField(
        label="Security Answer", max_length=100, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
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

            user.save()
            user_student = Student(occupation=self.cleaned_data['occupation'],
                                   security_question=self.cleaned_data["security_question"], security_answer=self.cleaned_data['security_answer'], birthday=self.cleaned_data['birthday'], user=user)
            user_student.save()

        return user


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):

    field_order = ['new_password1', 'new_password2']
