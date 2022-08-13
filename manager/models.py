from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

from manager.validators import address_regex_validator, city_name_regex_validator, phone_regex_validator, \
    postcode_regex_validator


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='nazwa kategorii')

    class Meta:
        verbose_name = _('Kategoria')
        verbose_name_plural = _('Kategorie')

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name


class Institution(models.Model):
    TYPES = {
        (1, 'Fundacja'),
        (2, 'Organizacja Pozarządowa'),
        (3, 'Zbiórka Lokalna'),
    }

    name = models.CharField(max_length=255, verbose_name='nazwa')
    description = models.TextField(verbose_name='cel organizacji')
    type = models.PositiveIntegerField(choices=TYPES, default=1, verbose_name='status organizacji')
    categories = models.ManyToManyField(Category, verbose_name='kategorie artykułów przyjmowane przez organizację')

    class Meta:
        verbose_name = _('Organizacja')
        verbose_name_plural = _('Organizacje')
        ordering = ('name', 'type', 'description',)

    def natural_key(self):
        return f'{self.get_type_display()} "{self.name}"'

    def __str__(self):
        return f'{self.get_type_display()} "{self.name}"'


class Donation(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='ilość worków')
    categories = models.ManyToManyField(Category, verbose_name='kategorie artykułu')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='instytucja obdarowywana')
    address = models.CharField(
        max_length=100, verbose_name='adres zamieszkania', validators=[address_regex_validator]
    )
    phone_number = models.CharField(max_length=16, verbose_name='nr telefonu', validators=[phone_regex_validator])
    city = models.CharField(max_length=100, verbose_name='miasto', validators=[city_name_regex_validator])
    zip_code = models.CharField(max_length=6, verbose_name='kod pocztowy', validators=[postcode_regex_validator])
    pick_up_date = models.DateField(verbose_name='data odbioru')
    pick_up_time = models.TimeField(verbose_name='czas odbioru')
    pick_up_comment = models.TextField(verbose_name='komentarz')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, default=None, verbose_name='użytkownik'
    )
    is_taken = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Darowizna')
        verbose_name_plural = _('Darowizny')
        ordering = ('is_taken', '-pick_up_date', '-pick_up_time', 'quantity',)

    def __str__(self):
        return f'#{self.id}'