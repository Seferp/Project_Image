from .models import Images, UserProfile
from rest_framework import serializers

class ImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('image')


class UserProfileSerializers(serializers.ModelSerializer):
    images = ImagesSerializers(many=True, read_only=True)
    class Meta:
        model = UserProfile
        field = ('id', 'user', 'plan', 'images')
