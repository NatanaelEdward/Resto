from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from menuapp.models import ProfitSummary,DataMenu,PenjualanDetail
from django.db.models import Sum,Count
from datetime import datetime, timedelta
from django.utils import timezone


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

    profit_summaries = ProfitSummary.objects.all()

    total_profit_today = None
    most_popular_food = None
    monthly_profits = None

    # Check if a date is specified in the request
    specific_date = request.GET.get('date')
    if specific_date:
        # Convert the provided date string to a datetime object
        specific_date = datetime.strptime(specific_date, '%Y-%m-%d').date()

        # Filter ProfitSummary objects for the provided date
        total_profit_today = ProfitSummary.objects.filter(created_at__date=specific_date).aggregate(total_profit=Sum('profit'))

    # Monthly profits calculation
    current_month_start = datetime.today().replace(day=1).date()
    monthly_end = current_month_start + timedelta(days=30)
    monthly_profits = ProfitSummary.objects.filter(created_at__date__range=[current_month_start, monthly_end]) \
        .values('created_at__date').annotate(total_profit=Sum('profit'))

    # Calculating most popular food
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
    })
