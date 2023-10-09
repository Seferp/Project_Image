from .models import UploadImage
from rest_framework import serializers
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



class UploadImageBasicSerializer(serializers.ModelSerializer):
    img_200 = serializers.SerializerMethodField()
    class Meta:
        model = UploadImage
        fields = ['image', 'img_200']

    def get_img_200(self, obj):
        return self.context['request'].build_absolute_uri(obj.img_200.url) if obj.img_200 else None


    def create(self, validated_data):
        image = validated_data.pop('image')
        img_200 = self.create_thumbnail(image, size=(200, 200))

        upload_image = UploadImage.objects.create(image=image, img_200=img_200, **validated_data)
        return upload_image

    def create_thumbnail(self, image, size):
        img = Image.open(image)
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        thumbnail = InMemoryUploadedFile(thumb_io, None, f'{image.name.split(".")[0]}_thumb.jpg', 'image/jpeg',
                                         thumb_io.tell(), None)
        return thumbnail


class UploadImagePremiumEnterpriseSerializer(serializers.ModelSerializer):
    img_200 = serializers.SerializerMethodField()
    img_400 = serializers.SerializerMethodField()

    class Meta:
        model = UploadImage
        fields = ['image', 'img_200','img_400']

    def get_img_200(self, obj):
        return self.context['request'].build_absolute_uri(obj.img_200.url) if obj.img_200 else None

    def get_img_400(self, obj):
        return self.context['request'].build_absolute_uri(obj.img_400.url) if obj.img_400 else None

    def create(self, validated_data):
        image = validated_data.pop('image')
        img_200 = self.create_thumbnail(image, size=(200, 200))
        img_400 = self.create_thumbnail(image, size=(400, 400))

        upload_image = UploadImage.objects.create(image=image, img_200=img_200, img_400=img_400, **validated_data)
        return upload_image

    def create_thumbnail(self, image, size):
        img = Image.open(image)
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')
        thumbnail = InMemoryUploadedFile(thumb_io, None, f'{image.name.split(".")[0]}_thumb.jpg', 'image/jpeg', thumb_io.tell(), None)
        return thumbnail
