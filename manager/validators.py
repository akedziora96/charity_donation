import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from faker import Faker
fake = Faker("pl_PL")


def address_regex_validator(address):
    """Checks if phone number is propper formated"""
    address = address.strip()
    pattern = (
        r'^((([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+|\d{0,4})'
        r'\.?([-|\s]?(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])*)|\d{0,4})*\s\d{0,5}\/?\d{0,5}[a-zA-Z]?)$'
    )
    if not re.fullmatch(pattern, address):
        raise ValidationError(_("Nieprawidłowy adres"), code='invalid address')

    address = address.title()
    if '-' in address:
        address = '-'.join(word.capitalize() for word in address.split('-'))

    return address


def city_name_regex_validator(city_name):
    """Checks if phone number is propper formated"""
    city_name = city_name.strip()
    pattern = r'^(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+([-|\s]?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])*)*)$'
    if not re.fullmatch(pattern, city_name):
        raise ValidationError(_('Nieprawidłowa nazwa miasta.'), code='invalid city')
    city_name = city_name.title()
    if '-' in city_name:
        city_name = '-'.join(word.capitalize() for word in city_name.split('-'))

    return city_name


def postcode_regex_validator(postcode):
    """Checks if phone number is propper formated"""
    postcode = postcode.strip()
    pattern = r'^((\d{2}-\d{3})|\d{5})$'
    if not re.fullmatch(pattern, postcode):
        raise ValidationError(_('Nieprawidłowy kod pocztowy.'), code='invalid postcode')
    return postcode


def phone_regex_validator(phone_number):
    """Checks if phone number is propper formated"""
    phone_number = phone_number.replace('-', ' ').strip()
    phone_number_to_check = phone_number.replace(' ', '')

    pattern = (
        r'(?:(?:(?:\+|00)?48)|(?:\(\+?48\)))?(?:1[2-8]|2[2-69]|3[2-49]|4[1-8]|5[0-9]|6[0-35-9]|[7-8][1-9]|9[145])\d{7}'
    )
    if not re.fullmatch(pattern, phone_number_to_check):
        raise ValidationError(
            _('Nieprawidłowy kod pocztowy'), code='invalid phone number'
        )
    return phone_number

