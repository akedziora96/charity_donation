import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def name_regex_validator(name, order, code):
    pattern = r'^(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+(-{1}[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]+)?)$'

    if not re.fullmatch(pattern, name):
        raise ValidationError(_(f'Nieprawidłowe {order}.'), code=code)

    name = name.lower()

    if '-' in name:
        name = '-'.join(word.capitalize() for word in name.split('-'))
    else:
        name = name.capitalize()

    return name


def first_name_regex_validator(first_name):
    return name_regex_validator(name=first_name, order='imię', code='invalid first name')


def last_name_regex_validator(last_name):
    return name_regex_validator(name=last_name, order='nazwisko', code='invalid last name')