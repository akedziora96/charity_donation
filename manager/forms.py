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


class AnnonymousMailContactForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Wiadomość'}))


class LoggedUserMailContactForm(forms.Form):
    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Wiadomość'}))