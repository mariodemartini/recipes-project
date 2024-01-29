from django.shortcuts import render, redirect

from django.http import Http404
from django.contrib import messages
from django.urls import reverse

from .forms import RegisterForm, LoginForm

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    
    post = request.POST
    request.session['register_form_data'] = post
    form = RegisterForm(post)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Seu usuário foi criado, faça login.')

        del(request.session['register_form_data'])

    return redirect('authors:register')
    # return render(request, 'authors/pages/register_view.html', {
    #     'form': form,
    # })

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    return render(request, 'authors/pages/login.html')


