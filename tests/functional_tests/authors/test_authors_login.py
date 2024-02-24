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

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        # User open login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User see form page
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Send invalid datas
        username = self.get_by_placeholder(form, 'Usuário')
        password = self.get_by_placeholder(form, 'Senha')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # Send form
        form.submit()

        # User see error message
        self.assertIn(
            'Usuário e/ou senha inválidos',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_empty(self):
        # User open login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User see form page
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Empty fields
        username = self.get_by_placeholder(form, 'Usuário')
        password = self.get_by_placeholder(form, 'Senha')
        username.send_keys(' ')
        password.send_keys(' ')

        # Send form
        form.submit()

        # User see error message
        self.assertIn(
            'Usuário e/ou senha inválidos',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user'
            },
            follow=True
        )

        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'my_user'
            },
            follow=True
        )

        self.assertIn(
            'Deslogado com sucesso.',
            response.content.decode('utf-8')
        )

