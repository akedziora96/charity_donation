import re

from django.core.exceptions import ValidationError


def name_regex_validator(name, order):
    pattern = r'^(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+(-{1}[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]+)?)$'

    if not re.fullmatch(pattern, name):
        raise ValidationError(f"Podaj poprawne {order}.")

    name = name.lower()

    if '-' in name:
        name = '-'.join(word.capitalize() for word in name.split('-'))
    else:
        name = name.capitalize()

    return name


def first_name_regex_validator(first_name):
    return name_regex_validator(name=first_name, order='imię')


def last_name_regex_validator(last_name):
    return name_regex_validator(name=last_name, order='nazwisko')