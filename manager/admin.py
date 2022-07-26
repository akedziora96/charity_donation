from django.contrib import admin

from .models import Category, Institution, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Institution)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Donation)
class CategoryAdmin(admin.ModelAdmin):
    pass