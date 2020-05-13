from django.contrib import admin

# Register your models here.
from apps.models import UserInfo, Students

admin.site.register(UserInfo)
admin.site.register(Students)