from django.urls import reverse
from authors.forms import RegisterForm
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Digite seu nome de usuário'),
        ('email', 'Digite seu e-mail'),
        ('first_name', 'Digite seu nome'),
        ('last_name', 'Digite seu sobrenome'),
        ('password', 'Digite sua senha'),
        ('confirm', 'Repita sua senha'),
    ])
    def test_fiels_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)


    @parameterized.expand([
        ('username', (
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.')),
        ('password', (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. '
            'Mínimo de 8 caracteres.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    
    @parameterized.expand([
        ('username', 'Usuário'),
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'Email'),
        ('password', 'Senha'),
        ('confirm', 'Confirmar'),
    ])
    def test_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'confirm': 'Str0ngP@ssword1',
        }

        return super().setUp(*args, **kwargs)


    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
        ('first_name', 'Digite seu nome'),
        ('last_name', 'Digite seu sobrenome'),
        ('password', 'Senha obrigatória'),
        ('confirm', 'Senha obrigatória'),
        ('email', 'Email obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

