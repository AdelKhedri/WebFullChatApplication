from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .models import User
from time import sleep


class SeleniumTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        user = User.objects.create(phone_number=9123456789, username='sahar')
        user.set_password('sahar1234')
    
    @classmethod
    def tearDownClass(cls):
        # cls.selenium.quit()
        super().tearDownClass()
    
    @classmethod
    def test_browser_login(self):
        self.selenium.get(f'{self.live_server_url}/login/')
        phone_number_input = self.selenium.find_element(By.NAME, 'phone_number')
        phone_number_input.send_keys(9123456789)
        password_input = self.selenium.find_element(By.NAME, 'password')
        password_input.send_keys('sahar1234')
        # button_sum = self.selenium.find_element(By.XPATH, '//button[text="ورود"]').click()