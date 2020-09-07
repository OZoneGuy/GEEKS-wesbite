from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.contrib.auth.models import User as U


# Create your models here.
class User(models.Model):
    user = models.OneToOneField(U,
                                on_delete=models.CASCADE,
                                primary_key=True)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,
                               label="Username")
    f_name = forms.CharField(max_length=50,
                             label="First Name")
    l_name = forms.charField(max_length=50,
                             label="Last Name")
    email = forms.EmailField(label="McMaster Email")
    password = forms.CharField(min_length=8,
                               widget=forms.PasswordWidget,
                               label="Password")
    rep_password = forms.CharField(min_length=8,
                                   widget=forms.PasswordWidget,
                                   label="Repeat Password")

    def clean_email(self):
        domain = self.cleaned_data['email'].split('@')[-1]
        if (domain.lower() != "mcmaster.ca"):
            raise ValidationError(
                "Invalid email. Please use your McMaster email.")
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super.clean()
        password = cleaned_data.get('password')
        rep_password = cleaned_data.get('rep_password')

        if rep_password != password:
            self.add_error('rep_password', ValidationError(
                "Passwords do not match."))
