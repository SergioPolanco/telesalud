# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
# Create your views here.

# def login_render(request):
#     return render(request, 'login/login.html')
    

def login_view(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    print("entro al login")
    if request.user.is_authenticated():
        print("esta logeado")
        return redirect(reverse('dashboardView'))
    print("esta logeado")
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = bool(request.POST.get('remember'))
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if not remember:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                else:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                login(request, user)
                return redirect(reverse('login'))
            else:
                # Redireccionar informando que la cuenta esta inactiva
                pass
        mensaje = 'Usuario y/o contraseña incorrecta.'
    return render(request, 'login/login.html', {'mensaje': mensaje})
    

def logout_view(request):
    logout(request)
    print("entro al logout")
    return redirect(reverse('loginView'))