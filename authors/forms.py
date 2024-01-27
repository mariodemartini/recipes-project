import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. '
            'Mínimo de 8 caracteres.'
        ), 
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['email'], 'Digite seu e-mail')
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['confirm'], 'Repita sua senha')

    first_name = forms.CharField(
        error_messages={'required': 'Digite seu nome'},
        label='Nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Digite seu sobrenome'},
        label='Sobrenome'
    )
    email = forms.EmailField(
        error_messages={'required': 'Email obrigatório'},
        label='E-mail',
        help_text='Digite um email válido.',
    )
    password = forms.CharField(
        required=True,
        label='Senha',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Senha obrigatória'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. '
            'Mínimo de 8 caracteres.'
        ),
        validators=[strong_password]
    )
    confirm = forms.CharField(
        required=True,
        label='Confirmar',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Senha obrigatória'
        },
    )


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário',
            'email': 'Email',
            'password': 'Senha',
        }
        error_message = {
            'username': {
                'required': 'Campo Obrigatório',
            }
        }
        # help_text = {
        #     'email': 'Digite um email válido.',
        # }
        # widgets = {
        #     'first_name': forms.TextInput(attrs={
        #         'placeholder': 'Digite seu nome'
        #     })
        # }

    # EXEMPLE VALIDATION ERROR WITH PASSWORD
    # def clean_password(self):
    #     data = self.cleaned_data.get('password')
    #     if 'atenção' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo password',
    #             code='invalid',
    #             params={'value': '"atenção"'}
    #         )
    #     return data


    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm')

        if password != confirm:
            password_confirmation_error = ValidationError(
                'As senhas não conferem. Digite novamente!',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'confirm': [
                    password_confirmation_error,
                ],
            })
        
