# Register your models here.
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'email', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Importants Dates', {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'email', 'phone_number', 'profile_picture')
        })
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','phone_number','profile_picture')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-username',)
