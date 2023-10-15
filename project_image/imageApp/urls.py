from django.urls import path
from .views import UploadImageList, DownloadImageView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('images/', UploadImageList.as_view(), name='image-list'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('api/images/<int:pk>/download/', DownloadImageView.as_view(), name='download_image'),

]
