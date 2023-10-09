from .models import UploadImage
from .serializers import UploadImageBasicSerializer, UploadImagePremiumEnterpriseSerializer
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.


class UploadImageList(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user_profile = self.request.user.userprofile
        if user_profile.plan in ['Premium', 'Enterprise']:
            return UploadImagePremiumEnterpriseSerializer
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

        return super().list(request, *args, **kwargs)