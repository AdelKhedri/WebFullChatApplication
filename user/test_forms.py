from .forms import UserCreateForm, UserLoginForm
from django.test import TestCase
from django.urls import reverse
from .models import User


class UserCreateFormTest(TestCase):
    def setUp(self):
        user = User.objects.create(phone_number=9123456789, username='test')
        pass

    def test_form_field_attrebutes(self):
        form = UserCreateForm()
        self.assertEqual(form.fields['phone_number'].help_text, '')
        self.assertIsNone(form.fields['phone_number'].initial)
    
    def test_valid_form(self):
        form = UserCreateForm({'username': 'test2', 'phone_number': 9929941452, 'password': 'test1234', 'password2': 'test1234'})
        self.assertTrue(form.is_valid())
    
    def test_error_text(self):
        data = {
            'phone_number': 9123456789,
            'username': 'test',
            'password': 'test123',
            'password2': 'test123w',
        }
        res = self.client.post(reverse('user:sinup'), data)
        self.assertFormError(res.context['form'], 'phone_number', 'این شماره تکراری است')
        self.assertFormError(res.context['form'], 'username', 'این یوزرنیم تکراری است')


class UserLoginFormTest(TestCase):
    def setUp(self):
        User.objects.create(phone_number=9123456789, username='test')

    def test_field_attrebuts(self):
        form = UserLoginForm()
        self.assertEqual(form.fields['phone_number'].help_text, '9123456789')
        self.assertEqual(form.fields['phone_number'].initial, None)

    def test_form_valid(self):
        form = UserLoginForm({'phone_number': 9123456789, 'password': 'test1234'})
        self.assertTrue(form.is_valid())
    
    def test_error_text(self):
        data = {
            'phone_number': 91234567891,
            'password': '1234'
            }
        res = self.client.post(reverse('user:login'), data)
        self.assertFormError(res.context['form'], 'phone_number', 'شماره تلفن وجود ندارد')
        self.assertFormError(res.context['form'], 'password', 'پسورد نباید کمتر از 8 کاراکتر باشد')