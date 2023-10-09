from django.contrib import admin
from .models import  UserProfile, UploadImage

# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['profile', 'plan']

class UploadImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UploadImage, UploadImageAdmin)