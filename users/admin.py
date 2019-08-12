from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')





admin.site.register(User, UserAdmin)
