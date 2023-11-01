from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from menuapp.models import ProfitSummary,DataMenu,PenjualanDetail
from django.db.models import Sum,Count
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import TruncMonth
from calendar import monthrange
from menuapp.models import KelompokMenu,JenisMenu,HargaMenu,JenisSize,BahanMenu
from menuapp.forms import DataMenuForm,HargaMenuForm,BahanMenuForm,DataMenuEditForm

def menu_view(request):
    all_datamenu = DataMenu.objects.all()
    return render(request, 'admin/menu.html', {'all_datamenu': all_datamenu})

def add_data_menu(request):
    if request.method == 'POST':
        form = DataMenuForm(request.POST, request.FILES)
        if form.is_valid():
            data_menu = form.save(commit=False)

            kelompok_menu_id = request.POST.get('kelompok_menu')
            jenis_menu_id = request.POST.get('jenis_menu')  
            jenis_size_id = request.POST.get('jenis_size')
            harga_menu_value = request.POST.get('harga_menu')

            kelompok_menu = KelompokMenu.objects.get(id=kelompok_menu_id)
            jenis_menu = JenisMenu.objects.get(id=jenis_menu_id)
            jenis_size = JenisSize.objects.get(id=jenis_size_id)

            data_menu.kelompok_menu = kelompok_menu
            data_menu.jenis_menu = jenis_menu
            data_menu.jenis_size = jenis_size
            data_menu.save()  # Save the DataMenu first to obtain an ID

            # Create a new HargaMenu instance and link it to the selected DataMenu and JenisSize
            harga_menu = HargaMenu.objects.create(menu=data_menu, size=jenis_size, harga_menu=harga_menu_value)

            return redirect(add_data_menu)  # Redirect to success page after form submission

    else:
        form = DataMenuForm()

    return render(request, 'admin/tambahMenu.html', {'form': form})

def edit_menu(request, id):
    data_menu = get_object_or_404(DataMenu, id=id)
    if request.method == 'POST':
        form = DataMenuEditForm(request.POST, instance=data_menu)
        if form.is_valid():
            form.save()
            return redirect('menu_view')  # Redirect to the menu list page
    else:
        form = DataMenuEditForm(instance=data_menu)
    return render(request, 'admin/editMenu.html', {'form': form, 'data_menu': data_menu})

# Delete menu view
def hapus_menu(request, id):
    data_menu = get_object_or_404(DataMenu, id=id)
    if request.method == 'POST':
        data_menu.delete()
        return redirect('menu_view')  # Redirect to the menu list page
    return render(request, 'admin/hapusMenu.html', {'data_menu': data_menu})

def update_price(request, id):
    menu = get_object_or_404(DataMenu, pk=id)
    harga_menus = menu.hargamenu_set.all()

    if request.method == 'POST':
        form = HargaMenuForm(request.POST)
        if form.is_valid():
            harga_menu = form.save(commit=False)
            existing_harga_menu = harga_menus.filter(size=harga_menu.size).first()

            if existing_harga_menu:
                existing_harga_menu.harga_menu = harga_menu.harga_menu
                existing_harga_menu.save()
            else:
                harga_menu.menu = menu
                harga_menu.save()
                
            return redirect('menu_view')
    else:
        form = HargaMenuForm()

    return render(request, 'admin/updateprice.html', {'form': form, 'menu': menu, 'harga_menus': harga_menus})


@login_required
def laporanAdmin(request):
    if request.user.userprofile.role != 'admin':
        return redirect('login_view')

    profit_summaries = ProfitSummary.objects.all()

    total_profit_today = None
    most_popular_food = None
    monthly_profits = None
    specific_date = None

    day_selected = request.GET.get('day')

    if day_selected:
        specific_date = datetime.strptime(day_selected, '%Y-%m-%d').date()
        total_profit_today = ProfitSummary.objects.filter(created_at__date=specific_date).aggregate(total_profit=Sum('profit'))

    monthly_profits = (
        ProfitSummary.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_profit=Sum('profit'))
        .order_by('month')
    )

    total_quantity_per_menu = PenjualanDetail.objects.values('kode_menu').annotate(total_qty=Sum('qty_menu')).order_by('-total_qty')[:1]
    most_popular_food = []
    for item in total_quantity_per_menu:
        menu = DataMenu.objects.get(pk=item['kode_menu'])
        menu.total_qty_sold = item['total_qty']
        most_popular_food.append(menu)

    return render(request, 'Admin/laporanAdmin.html', {
        'profit_summaries': profit_summaries,
        'total_profit_today': total_profit_today,
        'most_popular_food': most_popular_food,
        'monthly_profits': monthly_profits,
        'specific_date': specific_date,
    })

#bahan menu
def add_ingredient(request, menu_id):
    menu = get_object_or_404(DataMenu, pk=menu_id)

    if request.method == 'POST':
        form = BahanMenuForm(request.POST)
        if form.is_valid():
            bahan_menu = form.save(commit=False)
            bahan_menu.menu = menu
            bahan_menu.save()
            return redirect('menu_detail', menu_id=menu_id)  # Redirect to menu detail view
    else:
        form = BahanMenuForm()

    return render(request, 'add_ingredient.html', {'form': form, 'menu': menu})

def edit_ingredient(request, menu_id, ingredient_id):
    menu = get_object_or_404(DataMenu, pk=menu_id)
    ingredient = get_object_or_404(BahanMenu, pk=ingredient_id)

    if request.method == 'POST':
        form = BahanMenuForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', menu_id=menu_id)  # Redirect to menu detail view
    else:
        form = BahanMenuForm(instance=ingredient)

    return render(request, 'edit_ingredient.html', {'form': form, 'menu': menu, 'ingredient': ingredient})

def delete_ingredient(request, menu_id, ingredient_id):
    menu = get_object_or_404(DataMenu, pk=menu_id)
    ingredient = get_object_or_404(BahanMenu, pk=ingredient_id)
    
    if request.method == 'POST':
        ingredient.delete()
        return redirect('menu_detail', menu_id=menu_id)  # Redirect to menu detail view

    return render(request, 'delete_ingredient.html', {'menu': menu, 'ingredient': ingredient})

