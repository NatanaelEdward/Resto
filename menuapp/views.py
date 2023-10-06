# menuapp/views.py
import json
import random
from django.shortcuts import render, redirect
from .forms import DataMenuForm
from django.http import JsonResponse
from .models import DataMenu, JenisMenu,PenjualanDetail,HargaMenu,JenisSize
from decimal import Decimal

def index_makanan(request):
    kategori = request.GET.get('kategori', '')  # Mendapatkan nilai parameter kategori dari URL
    menus = DataMenu.objects.filter(jenis_menu__nama_jenis=kategori)

    return render(request, 'user/indexMakanan.html', {'menus': menus, 'kategori': kategori})

def index_minuman(request):
    kategori = request.GET.get('kategori', '')  # Mendapatkan nilai parameter kategori dari URL
    menus = DataMenu.objects.filter(jenis_menu__nama_jenis=kategori)

    return render(request, 'user/indexMinuman.html', {'menus': menus, 'kategori': kategori})
def tambah_menu(request):
    if request.method == 'POST':
        form = DataMenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tambah_menu')  # Ganti 'daftar_menu' dengan nama URL daftar menu Anda.
    else:
        form = DataMenuForm()
    return render(request, 'Admin/tambahMenu.html', {'form': form})


