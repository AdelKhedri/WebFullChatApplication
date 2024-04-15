from django.test import TestCase
from .views import SinUpView, LoginView
from django.urls import resolve, reverse
from .models import User


class LoginViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number=9123456789, username='abas')
        user.set_password('abas1234')
        user.save()
        pass

    def test_exist_url(self):
        res = self.client.get('/login/')
        self.assertEqual(res.status_code, 200)
    
    def test_url_name(self):
        url = reverse('user:login')
        self.assertEqual(resolve(url).app_name, 'user')
        self.assertEqual(resolve(url).view_name, 'user:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)
        self.assertEqual(resolve(url).url_name, 'login')
    
    def test_template_name(self):
        res = self.client.get(reverse('user:login'))
        self.assertTemplateUsed(res, 'user/login.html')
    
    def test_login(self):
        res = self.client.login(phone_number=9123456789, password='abas1234')
        self.assertTrue(res)
        res = self.client.get(reverse('user:login'))
        self.assertIsInstance(res.context['user'], User)
        self.assertEqual(res.context['user'].username, 'abas')


class SinUpViewTest(TestCase):
    def setUp(self):
        pass

    def test_exist_url(self):
        res  = self.client.get(reverse('user:sinup'))
        self.assertEqual(res.status_code, 200)
    
    def test_url_name(self):
        url = reverse('user:sinup')
        self.assertEqual(resolve(url).view_name, 'user:sinup')
        self.assertEqual(resolve(url).url_name, 'sinup')
    
    def test_template_name(self):
        res = self.client.get(reverse('user:sinup'))
        self.assertTemplateUsed(res, 'user/sinup.html')