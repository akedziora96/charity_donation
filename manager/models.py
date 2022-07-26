from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='nazwa kategorii')


class Institution(models.Model):
    TYPES = {
        (1, 'fundacja'),
        (2, 'organizacja pozarządowa'),
        (3, 'zbiórka lokalna'),
    }

    name = models.CharField(max_length=255, verbose_name='nazwa')
    description = models.TextField(verbose_name='opis')
    type = models.PositiveIntegerField(choices=TYPES, default=1, verbose_name='status organizacji')
    categories = models.ManyToManyField(Category, verbose_name='kategorie artykułów przyjmowane przez organizację')


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, verbose_name='kategorie artykułu')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='instytucja przyjmująca')
    adress = models.CharField(max_length=100, verbose_name='adres zamieszkania')
    phone_number = models.CharField(max_length=15, verbose_name='nr telefonu')
    city = models.CharField(max_length=100, verbose_name='miasto')
    zip_code = models.CharField(max_length=6, verbose_name='kod pocztowy')
    pick_up_date = models.DateField(verbose_name='data odbioru')
    pick_up_time = models.TimeField(verbose_name='czas odbioru')
    pick_up_comment = models.DateTimeField(verbose_name='data komentarza')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name='użytkownik'
    )