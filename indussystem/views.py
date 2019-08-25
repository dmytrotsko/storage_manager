from django.contrib import auth
from django.contrib.auth import logout as django_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from global_login_required import login_not_required


def index(request):
    return render(request, 'index.html')

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
