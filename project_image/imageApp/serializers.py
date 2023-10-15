from .models import UploadImage
from rest_framework import serializers
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from datetime import datetime


class UploadImageBasicSerializer(serializers.ModelSerializer):
    image_200 = serializers.SerializerMethodField()

    class Meta:
        model = UploadImage
        fields = ['image', 'image_200']

    def get_image_200(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_200.url) if obj.image_200 else None

    def create(self, validated_data):
        image = validated_data.pop('image')
        img_200 = self.create_thumbnail(image, size=(200, 200))
        upload_image = UploadImage.objects.create(image=image, image_200=img_200, **validated_data)
        return upload_image

    def create_thumbnail(self, image, size):
        img = Image.open(image)
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        thumbnail = InMemoryUploadedFile(thumb_io, None, f'{image.name.split(".")[0]}_thumb.jpg', 'image/jpeg',
                                         thumb_io.tell(), None)
        return thumbnail


class UploadImagePremiumSerializer(serializers.ModelSerializer):
    image_200 = serializers.SerializerMethodField()
    image_400 = serializers.SerializerMethodField()

    class Meta:
        model = UploadImage
        fields = ['image', 'image_200', 'image_400']

    def get_image_200(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_200.url) if obj.image_200 else None

    def get_image_400(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_400.url) if obj.image_400 else None

    def create(self, validated_data):
        image = validated_data.pop('image')
        image_200 = self.create_thumbnail(image, size=(200, 200))
        image_400 = self.create_thumbnail(image, size=(400, 400))

        upload_image = UploadImage.objects.create(
            image=image,
            image_200=image_200,
            image_400=image_400,
            **validated_data
        )

        return upload_image

    def create_thumbnail(self, image, size):
        img = Image.open(image)
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        thumbnail = InMemoryUploadedFile(thumb_io, None, f'{image.name.split(".")[0]}_thumb.jpg', 'image/jpeg',
                                         thumb_io.tell(), None)
        return thumbnail


class UploadImageEnterpriseSerializer(serializers.ModelSerializer):
    image_200 = serializers.SerializerMethodField()
    image_400 = serializers.SerializerMethodField()
    expired_link = serializers.SerializerMethodField()
    expired_time = serializers.IntegerField(min_value=300, max_value=30000)

    class Meta:
        model = UploadImage
        fields = ['image', 'image_200', 'image_400', 'expired_link', 'expired_time', 'added_date']

    def get_image_200(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_200.url) if obj.image_200 else None

    def get_image_400(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_400.url) if obj.image_400 else None

    def create(self, validated_data):
        image = validated_data.pop('image')
        image_200 = self.create_thumbnail(image, size=(200, 200))
        image_400 = self.create_thumbnail(image, size=(400, 400))

        upload_image = UploadImage.objects.create(
            image=image,
            image_200=image_200,
            image_400=image_400,
            **validated_data
        )

        return upload_image

    def create_thumbnail(self, image, size):
        img = Image.open(image)
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        thumbnail = InMemoryUploadedFile(thumb_io, None, f'{image.name.split(".")[0]}_thumb.jpg', 'image/jpeg',
                                         thumb_io.tell(), None)
        return thumbnail

    def get_expired_link(self, obj):
        download_url = reverse('download_image', kwargs={'pk': obj.id})
        return self.context['request'].build_absolute_uri(download_url)
