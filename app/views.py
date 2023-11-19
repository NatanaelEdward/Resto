from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from .decorators import role_required

role_to_view = {
    'manajer': 'indexAdmin',
    'kasir': 'indexKasir',
    'user': 'indexMakanan/',
    'admin': 'indexAdmin',
}

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            user_role = user.userprofile.role
            return redirect(role_to_view.get(user_role, 'login_view'))

    return render(request, 'Login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')

def err404(request, exception):
    return redirect('login_view')

def err500(request):
    return redirect('login_view')

def err403(request,exception):
    return redirect('login_view')

#Admin
@login_required
@role_required(allowed_roles=('manajer', 'admin'))
def indexAdmin(request):
        return render(request, 'Admin/index.html')

#Kasir
@login_required
@role_required(allowed_roles=('kasir','admin'))
def indexKasir(request):
        return render(request, 'Kasir/index.html')

#User
@login_required
@role_required(allowed_roles=('user',))
def indexUser(request):
    return render(request, 'User/indexMakanan.html')



def get_categories(request):
    url = 'https://www.themealdb.com/api/json/v1/1/categories.php'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Gagal mengambil data'}, status=500)