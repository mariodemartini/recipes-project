from django import forms
from django.contrib.auth.models import User


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['email'], 'Digite seu e-mail')
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')

    senha = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha'
        }),
        error_messages={
            'required': 'Senha obrigatória'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. '
            'Mínimo de 8 caracteres.'
        )
    )

    confirmar = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            # 'password',
        ]

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário',
            'email': 'E-mail',
        }

        help_text = {
            'email': 'Digite um email válido.',
        }

        error_message = {
            'username': {
                'required': 'Campo Obrigatório',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome'
            })
        }


