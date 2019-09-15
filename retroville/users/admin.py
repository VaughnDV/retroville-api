from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import ugettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    # ordering = ["email", "date_of_birth"]
    # fieldsets = ["firstname", "lastname", "is_active", "is_staff", "email", "date_of_birth"]
    # list_filter = ["date_of_birth"]
    # search_fields = ["email", "date_of_birth"]
    # exclude = ["username"]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # form = UserChangeForm
    # add_form = UserCreationForm
    # change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', "phone_number", "country_code")
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', "phone_number", "country_code")
    search_fields = ('email', 'date_of_birth', 'first_name', 'last_name, "phone_number", "country_code"')
    ordering = ('email', 'date_of_birth', 'first_name', 'last_name', "phone_number", "country_code")
