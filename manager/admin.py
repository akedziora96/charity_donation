from django.contrib import admin

from .forms import DonationAddForm
from .models import Category, Institution, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('name', 'type', 'description')
    search_fields = ('name',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    add_form = DonationAddForm
    form = DonationAddForm
    list_display = ('user', 'quantity', 'institution', 'pick_up_date', 'pick_up_time', 'is_taken', 'created')
    list_filter = ('user', 'quantity', 'institution', 'pick_up_date', 'pick_up_time', 'is_taken', 'created')
    search_fields = ('user', 'institution', 'created')
    date_hierarchy = 'pick_up_date'