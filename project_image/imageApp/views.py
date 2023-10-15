from .models import UploadImage
from .serializers import UploadImageBasicSerializer, UploadImagePremiumSerializer, UploadImageEnterpriseSerializer
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.http import HttpResponse, FileResponse
from datetime import timedelta


# Create your views here.


class UploadImageList(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user_profile = self.request.user.userprofile
        if user_profile.plan == 'Premium':
            return UploadImagePremiumSerializer
        elif user_profile.plan == 'Enterprise':
            return UploadImageEnterpriseSerializer
        else:
            return UploadImageBasicSerializer

    def get_queryset(self):
        return UploadImage.objects.filter(user=self.request.user.userprofile)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user.userprofile
        serializer.save()

    def list(self, request, *args, **kwargs):
        user_profile = self.request.user.userprofile
        if user_profile.plan == 'Basic':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            for item in data:
                del item['image']

            return Response(serializer.data)

        elif user_profile.plan == 'Enterprise':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            for item in data:
                del item['expired_time']
                # del item['added_date']

            return Response(serializer.data)

        return super().list(request, *args, **kwargs)


class DownloadImageView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UploadImage.objects.all()
    serializer = UploadImageEnterpriseSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        expiration_date = instance.added_date + timedelta(seconds=instance.expired_time)
        if expiration_date and expiration_date < timezone.now():
            return HttpResponse(status=400)

        print(f"Stara data {instance.added_date}")
        print(f"Nowa data {expiration_date}")


        response = FileResponse(instance.image, content_type="image/jpeg")
        response['Content-Disposition'] = f'attachment; filename="{instance.image.name}"'
        return response