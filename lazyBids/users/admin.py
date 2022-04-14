from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser) #Make custom user available on /admin/ page
# Register your models here.
