from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=[('Basic', 'Basic'), ('Premium', 'Premium'),
                                                    ('Enterprise', 'Enterprise')])


class UploadImage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    image_200 = models.ImageField(upload_to='thumbnails_200/', null=True, blank=True)
    image_400 = models.ImageField(upload_to='thumbnails_400/', null=True, blank=True)
    expired_link = models.URLField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now=True)
    expired_time = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_200:
            img_200 = Image.open(self.image_200.path)
            img_200.thumbnail((200, 200))
            img_200.save(self.image_200.path)

        if self.image_400:
            img_400 = Image.open(self.image_400.path)
            img_400.thumbnail((400, 400))
            img_400.save(self.image_400.path)

    def get_expired_time(self):
        return self.expired_time


@receiver(post_save, sender=UploadImage)
def generate_expired_link(sender, instance, **kwargs):

    if instance.image and not instance.expired_link:
        download_url = reverse('download_image', kwargs={'pk': instance.pk})
        instance.expired_link = f"http://127.0.0.1:8000{download_url}"
        instance.save()
