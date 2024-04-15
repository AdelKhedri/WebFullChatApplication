from django.test import TestCase
from .models import User, Profile

class UserModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user', phone_number=9929941452)
    
    def test_exist_user(self):
        user = User.objects.get(username='user', phone_number=9929941452)
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.phone_number, 9929941452)


class ProfileModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user', phone_number=9929941452)
        profile = Profile.objects.create(user=user, image='./images.jpg')
    
    def test_user_have_image(self):
        user = User.objects.get(username='user').profile
        self.assertTrue(user.has_image())