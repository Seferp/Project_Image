from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=[('Basic', 'Basic'), ('Premium', 'Premium'),
                                                    ('Enterprise', 'Enterprise')])


class UploadImage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    img_200 = models.ImageField(upload_to='thumbnails_200/', null=True, blank=True)
    img_400 = models.ImageField(upload_to='thumbnails_400/', null=True, blank=True)


