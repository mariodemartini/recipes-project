from authors.forms import RegisterForm
from django.test import TestCase
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

