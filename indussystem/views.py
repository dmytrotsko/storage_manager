from django.contrib import auth
from django.contrib.auth import logout as django_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from indussystem.parameters import add_parameters

from global_login_required import login_not_required


def index(request):
    villas = Villa.objects.all()
    ctx = {
        'villas': villas
    }

    return render(request, 'index.html', ctx)


def create_villa(request):
    if request.method == 'POST':
        villa_name = request.POST.get('villa_name')
        Villa.objects.create(name=villa_name)
        return redirect(add_parameters(request, villa=f'{villa_name}'))

    ctx = {'v': None}

    if request.GET.get('villa'):
        ctx['v'] = request.GET.get('villa')

    return render(request, 'create_villa.html', ctx)


@login_not_required
def login(request):
    """Shows a login form and a registration link."""

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")

        else:
            return HttpResponse("Invalid login. Please try again.")

    # if not POST then return login form
    return render(request, "login.html", {'next': ''})
