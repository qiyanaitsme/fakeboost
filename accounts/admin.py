from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "balance", "is_staff", "is_superuser")
    search_fields = ("username", "email")  
    ordering = ("id",)  

    fieldsets = (
        (None, {"fields": ("username", "email", "password", "balance")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
