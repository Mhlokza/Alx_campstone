from django.contrib import admin
from .models import CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin as DefaultAdmin

class UserAdmin(DefaultAdmin):
    list_display= ("email", "username")

admin.site.register(UserProfile)
admin.site.register(CustomUser, UserAdmin)



