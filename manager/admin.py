from django.contrib import admin
from .models import Category, Institution, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Institution)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('name', 'type', 'description')
    search_fields = ('name',)


@admin.register(Donation)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'institution', 'pick_up_date', 'pick_up_time')
    list_filter = ('user', 'quantity', 'institution', 'pick_up_date', 'pick_up_time')
    search_fields = ('user', 'institution')
    date_hierarchy = 'pick_up_date'