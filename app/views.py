from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request,'Kasir/index.html')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid login credentials.'})
#     else:
#         return render(request, 'login.html')

#test login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)
        if user:
            if user.is_active:
                login(request, user)
                if user.userprofile.role == 'kasir':
                    return render(request, 'Kasir/index.html', {'user': user})
                elif user.userprofile.role == 'admin':
                     return render(request, 'Admin/index.html', {'user': user})
        else:
            return render(request , 'Login.html')

    else:
        return render(request , 'Login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login_view')

def indexKasir(request):
    return render(request, 'Kasir/index.html')

def indexUser(request):
    return render(request, 'User/index.html')

def indexAdmin(request):
    return render(request, 'Admin/index.html')

