from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from .models import User
from .validators import first_name_regex_validator, last_name_regex_validator


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Hasło'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Powtórz Hasło'}
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name',)
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię', }),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'})
        }

    def clean_first_name(self):
        return first_name_regex_validator(first_name=self.cleaned_data.get('first_name'))

    def clean_last_name(self):
        return last_name_regex_validator(last_name=self.cleaned_data.get('last_name'))


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name',)

    def clean_first_name(self):
        return first_name_regex_validator(first_name=self.cleaned_data.get('first_name'))

    def clean_last_name(self):
        return last_name_regex_validator(last_name=self.cleaned_data.get('last_name'))


class CustomUserEditForm(CustomUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    class Meta(CustomUserChangeForm.Meta):
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'})
        }

    def clean_first_name(self):
        return first_name_regex_validator(first_name=self.cleaned_data.get('first_name'))

    def clean_last_name(self):
        return last_name_regex_validator(last_name=self.cleaned_data.get('last_name'))


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={'placeholder': 'E-mail'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Hasło'}
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Aktualne hasło'}
        )
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Podaj nowe hasło'}
        )
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Powtórz nowe hasło'}
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'E-mail'})

    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email').strip()
        if not User.objects.filter(email__icontains=email).exists():
            raise ValidationError(_('Konto użytkownika o podanym mailu nie istnieje!'), code='email_doesnt_exist')

        return email


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Podaj nowe hasło'}
        )
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Powtórz nowe hasło'}
        )

