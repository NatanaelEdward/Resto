from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request,'Kasir/index.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login_view')

def indexKasir(request):
    return render(request, 'Kasir/index.html')

def indexUser(request):
    return render(request, 'User/index.html')

def indexAdmin(request):
    return render(request, 'Admin/index.html')

