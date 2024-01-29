from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['email'], 'Digite seu e-mail')
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['confirm'], 'Repita sua senha')

    username = forms.CharField(
        label='Usuário',
        help_text=(
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.'
        ),
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'Usuário deve ter mínimo de 4 caracteres',
            'max_length': 'Usuário deve ter máximo de 150 caracteres',
        },
        min_length=4, max_length=150,
    )
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
        label='Email',
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Esse email já existe!', code='invalid',
            )

        return email


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
        