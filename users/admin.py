from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('email', 'first_name', 'last_name',  'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'
            )}),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    @receiver(pre_delete, sender=User)
    def delete_user(sender, instance, **kwargs):
        if instance.is_superuser and User.objects.filter(is_superuser=True).count() == 1:
            raise Exception('Nie można usunąć ostatniego admina.')


admin.site.register(User, CustomUserAdmin)
