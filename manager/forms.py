from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from users.validators import first_name_regex_validator, last_name_regex_validator
from .models import Donation

from django.utils.translation import gettext_lazy as _


class DonationAddForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
        exclude = ('user', )

    def clean_pick_up_date(self):
        pick_up_date = self.cleaned_data.get('pick_up_date')
        if not pick_up_date >= timezone.now().date():
            raise ValidationError(_('Podana data jest z przeszłości.'), code='date_from_past')

        return pick_up_date

    def clean(self):
        cleaned_data = super().clean()
        pick_up_date = cleaned_data.get('pick_up_date')
        pick_up_time = cleaned_data.get('pick_up_time')

        if not pick_up_date:
            raise ValidationError(_('Podana data jest z przeszłości.'), code='date_from_past')

        if pick_up_date <= timezone.now().date() and pick_up_time < timezone.now().time():
            raise ValidationError(_('Podana godzina jest z przeszłości.'), code='hour_from_past')

        return cleaned_data


class AnnonymousMailContactForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Wiadomość'}))

    def clean_first_name(self):
        return first_name_regex_validator(first_name=self.cleaned_data.get('first_name'))

    def clean_last_name(self):
        return last_name_regex_validator(last_name=self.cleaned_data.get('last_name'))


class LoggedUserMailContactForm(forms.Form):
    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Wiadomość'}))