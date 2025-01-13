from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# admin.site.register(User, UserAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_verified")
    list_filter = ("is_verified",)
    search_fields = ("username", "email")
