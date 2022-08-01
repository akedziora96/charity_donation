from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Donation


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class DonationAddForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
        exclude = ('user', )