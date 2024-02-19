import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        # User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see form page
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Usuário')
        password_field = self.get_by_placeholder(form, 'Senha')

        # User write username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User submit form
        form.submit()

        # User see login success message with username
        self.assertIn(
            f'Você está logado como {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )