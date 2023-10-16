from django.test import TestCase
from .models import UploadImage, UserProfile
from .views import UploadImageList, DownloadImageView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
import os


class ModelTest(TestCase):
    def setUp(self):
        image = Image.new('RGB', (600, 600), color='green')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)

        file_name = 'test_image.jpg'
        path = os.path.join('media', 'tests', file_name)
        with open(path, 'wb') as f:
            f.write(buffer.read())
        buffer.seek(0)
        uploaded_file = SimpleUploadedFile(file_name, buffer.read(), content_type='image/jpeg')

        self.user_enterprise = User.objects.create_user(username='testuser', password='testpassword')
        self.user_enterprise = UserProfile.objects.create(profile=self.user_enterprise, plan='Enterprise')
        self.test_image = UploadImage.objects.create(
            user=self.user_enterprise,
            image=uploaded_file,
            image_200=uploaded_file,
            image_400=uploaded_file
        )

    def test_image_thumbnail_generation(self):

        self.assertTrue(self.test_image.image_200)
        self.assertTrue(self.test_image.image_400)

        img_200 = Image.open(self.test_image.image_200.path)
        img_400 = Image.open(self.test_image.image_400.path)

        self.assertEqual(img_200.size, (200, 200))
        self.assertEqual(img_400.size, (400, 400))
    def test_expired_link_generation_signal(self):
        upload_image = UploadImage.objects.create(user=self.user_enterprise, image=self.test_image.image)
        upload_image.save()

        self.assertIsNotNone(upload_image.expired_link)

    def test_expired_link_generation_manual(self):
        upload_image = UploadImage.objects.create(user=self.user_enterprise, image=self.test_image.image)
        upload_image.save()

        download_url = reverse('download_image', kwargs={'pk': upload_image.pk})
        expected_expired_link = f"http://127.0.0.1:8000{download_url}"

        self.assertEqual(upload_image.expired_link, expected_expired_link)

    def test_get_expired_time(self):
        upload_image = UploadImage.objects.create(user=self.user_enterprise, image=self.test_image.image, expired_time=60)
        upload_image.save()

        self.assertEqual(upload_image.get_expired_time(), 60)

class url_test(TestCase):
    def test_url(self):
        self.assertEqual(resolve(reverse('image-list')).func.view_class, UploadImageList.as_view().view_class)
        self.assertEqual(resolve(reverse('download_image', kwargs={'pk': 1})).func.view_class, DownloadImageView.as_view().view_class)
        self.assertEqual(resolve(reverse('login')).func.view_class, LoginView.as_view().view_class)
        self.assertEqual(resolve(reverse('logout')).func.view_class, LogoutView.as_view().view_class)
