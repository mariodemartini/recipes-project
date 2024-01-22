from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    
    post = request.POST
    request.session['register_form_data'] = post
    form = RegisterForm(post)

    return redirect('authors:register')
    # return render(request, 'authors/pages/register_view.html', {
    #     'form': form,
    # })