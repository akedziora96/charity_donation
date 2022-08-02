from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nazwa kategorii')

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

    name = models.CharField(max_length=255, verbose_name='Nazwa')
    description = models.TextField(verbose_name='Cel organizacji')
    type = models.PositiveIntegerField(choices=TYPES, default=1, verbose_name='Status organizacji')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie artykułów przyjmowane przez organizację')

    class Meta:
        verbose_name = _('Organizacja')
        verbose_name_plural = _('Organizacje')

    def natural_key(self):
        return f'{self.get_type_display()} "{self.name}"'

    def __str__(self):
        return f'{self.get_type_display()} "{self.name}"'


class Donation(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='Ilość worków')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie artykułu')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja przyjmująca')
    address = models.CharField(max_length=100, verbose_name='Adres zamieszkania')
    phone_number = models.CharField(max_length=15, verbose_name='Nr telefonu')
    city = models.CharField(max_length=100, verbose_name='Miasto')
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(verbose_name='Data odbioru')
    pick_up_time = models.TimeField(verbose_name='Czas odbioru')
    pick_up_comment = models.TextField(verbose_name='Komentarz')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, default=None, verbose_name='Użytkownik'
    )
    is_taken = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name = _('Darowizna')
        verbose_name_plural = _('Darowizny')
        ordering = ('is_taken', '-pick_up_date', '-pick_up_time', 'quantity',)

    def __str__(self):
        return f'#{self.id}'