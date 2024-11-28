from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from .forms import EnergyUserCreationForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = EnergyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = EnergyUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid credentials'})

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return redirect('dashboard')
