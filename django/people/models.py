import uuid
from django import forms
from django.contrib.auth.models import User as U
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(U,
                                on_delete=models.CASCADE,
                                primary_key=True)
    is_member = models.BooleanField(default=False)
    member_code = models.UUIDField(editable=False)
    pending_member = models.BooleanField(defailt=False)

    class AccountTypes(models.TextChoices):
        MARKETING = 'MRKT', _('Marketing')
        EXEC = 'EXC', _('Exec')
        REGULAR = 'REG', _('Member')

    mem_type = models.CharField(max_length=2,
                                choices=AccountTypes.choices,
                                default=AccountTypes.REGULAR)

    @property
    def apply_for_membership(self):
        if (self.is_member):
            return
        self.pending_member = True
        self.save()
        return

    @property
    def make_member(self):
        if(self.is_member):
            return
        self.pending_member = False
        self.is_member = True
        self.member_code = uuid.uuid4()
        self.save()
        return

    class Meta:
        permissions = (
            ('can_make_member', 'Can give membership status')
        )


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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,
                               label="Username")
    password = forms.CharField(min_length=8,
                               widget=forms.PasswordWidget,
                               label="Password")
