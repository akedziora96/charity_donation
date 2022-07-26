from datetime import timedelta

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
        exclude = ('user', 'is_taken', 'created')

    def __init__(self, *args, **kwargs):
        """Enable to use User object in validation"""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pick_up_date = cleaned_data.get('pick_up_date')
        pick_up_time = cleaned_data.get('pick_up_time')

        if not pick_up_date or not pick_up_date:
            raise ValidationError(
                _('Brak wypełnionego pola z datą lub godziną lub obu pól.'), code='empty_date_time_fields'
            )

        if pick_up_date < timezone.now().date():
            raise ValidationError(
                _('Nieprawidłowa data odbioru. Wprowadzona data jest z przeszłości.'), code='date_from_past'
            )

        if pick_up_date <= timezone.now().date() and pick_up_time < timezone.localtime().time():
            raise ValidationError(
                _('Nieprawidłowa godzina odbioru. Wprowadzona godzina jest z przeszłości.'), code='hour_from_past'
            )

        user_last_submit = Donation.objects.filter(user=self.user).order_by('-created').first()
        if user_last_submit and timezone.now() - user_last_submit.created < timedelta(seconds=30):
            raise ValidationError(
                _('Nie można ponownie wysłać formularza od momentu jego poprzedniego wysłania.'), code='double_sent'
            )

        return cleaned_data


class AnnonymousMailContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(
            attrs={'id': 'id_contact_first_name', 'placeholder': 'Imię'}
        )
    )
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(
            attrs={'id': 'id_contact_last_name', 'placeholder': 'Nazwisko'}
        )
    )
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(
            attrs={'id': 'id_contact_email', 'placeholder': 'E-mail'}
        )
    )
    message = forms.CharField(
        max_length=1000, widget=forms.Textarea(
            attrs={'id': 'id_contact_message', 'placeholder': 'Wiadomość'}
        )
    )

    def clean_first_name(self):
        return first_name_regex_validator(first_name=self.cleaned_data.get('first_name'))

    def clean_last_name(self):
        return last_name_regex_validator(last_name=self.cleaned_data.get('last_name'))


class LoggedUserMailContactForm(forms.Form):
    message = forms.CharField(
        max_length=1000, widget=forms.Textarea(
            attrs={'id': 'id_contact_message', 'placeholder': 'Wiadomość'}
        )
    )