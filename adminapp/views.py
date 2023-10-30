from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse


def tambahMenu(request):
     if request.user.userprofile.role != 'admin':
             return redirect('login_view')
     return render(request, 'Admin/tambahMenu.html')

def editMenu(request):
     if request.user.userprofile.role != 'admin':
             return redirect('login_view')
     return render(request, 'Admin/editMenu.html')

def hapusMenu(request):
     if request.user.userprofile.role != 'admin':
             return redirect('login_view')
     return render(request, 'Admin/hapusMenu.html')

@login_required
def laporanAdmin(request):
        if request.user.userprofile.role != 'admin':
             return redirect('login_view')
        return render(request, 'Admin/laporanAdmin.html')



