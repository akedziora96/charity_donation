import re

from django.core.exceptions import ValidationError


def address_regex_validator(address):
    """Checks if phone number is propper formated"""
    pattern = r'^(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+([-|\s]?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])*)*\s\d{0,5}\/?\d{0,5}[a-zA-Z]?)$'
    if not re.fullmatch(pattern, address):
        raise ValidationError("Podaj poprawny adres.")

    address = address.title()
    if '-' in address:
        address = '-'.join(word.capitalize() for word in address.split('-'))

    return address


def city_name_regex_validator(city_name):
    """Checks if phone number is propper formated"""
    pattern = r'^(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+([-|\s]?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])*)*)$'
    if not re.fullmatch(pattern, city_name):
        raise ValidationError("Podaj poprawną nazwę miasta.")

    city_name = city_name.title()
    if '-' in city_name:
        city_name = '-'.join(word.capitalize() for word in city_name.split('-'))

    return city_name


def postcode_regex_validator(postcode):
    """Checks if phone number is propper formated"""
    pattern = r'^((\d{2}-\d{3})|\d{5})$'
    if not re.fullmatch(pattern, postcode):
        raise ValidationError("Podaj poprawny kod pocztowy.")
    return postcode


def phone_regex_validator(phone_number):
    """Checks if phone number is propper formated"""
    pattern = r'(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)'
    if not re.fullmatch(pattern, phone_number):
        raise ValidationError("Numer telefonu musi być podany w następującym formacie : '+999999999'.")
    return phone_number


