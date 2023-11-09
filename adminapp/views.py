from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from menuapp.models import ProfitSummary,DataMenu,PenjualanDetail,KelompokMenu,JenisMenu,HargaMenu,JenisSize,BahanMenu
from django.db.models import Sum,Count
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import TruncMonth
from calendar import monthrange
from menuapp.forms import DataMenuForm,HargaMenuForm,BahanMenuForm,DataMenuEditForm
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generate_monthly_pdf(request, year, month):
    profit_summary = ProfitSummary.objects.filter(
        created_at__year=year,
        created_at__month=month
    )

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF object using the BytesIO buffer
    p = canvas.Canvas(buffer, pagesize=letter)

    # Define the PDF content
    p.drawString(50, 750, f"Profit Summary for {month}/{year}")
    y = 720  # Initial Y-coordinate

    # Set headers
    headers = ["Menu", "Pendapatan Bersih", "Pendapatan Kotor", "Profit", "Tanggal"]
    for i, header in enumerate(headers):
        p.drawString(50 + i * 120, y, header)

    y -= 20  # Move to the next line

    # Loop through profit summaries and add content to the PDF
    for summary in profit_summary:
        menu = summary.menu.nama_menu_lengkap
        pendapatan_bersih = summary.pendapatan_bersih
        pendapatan_kotor = summary.pendapatan_kotor
        profit = summary.profit
        created_at = summary.created_at.strftime("%d-%m-%Y")  # Format date as per your need

        data = [menu, pendapatan_bersih, pendapatan_kotor, profit, created_at]

        for i, value in enumerate(data):
            p.drawString(50 + i * 120, y, str(value))

        y -= 20  # Move to the next line

    # Get the total profit for the month
    total_profit = sum(summary.profit for summary in profit_summary)

    # Add the total profit at the end of the document
    p.drawString(50, y, f"Total Profit for {month}/{year}: {total_profit}")

    # Save and close the PDF
    p.save()

    # Generate the response to send the PDF
    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="profit_summary_{year}_{month}.pdf"'
    return response

def generate_monthly_totals_pdf(request):
    months = ProfitSummary.objects.dates('created_at', 'month', order='DESC')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.drawString(50, 750, "Total Bulanan")
    y = 720  # Initial Y-coordinate

    headers = ["Month", "Total Bersih", "Total Kotor", "Total Profit"]
    for i, header in enumerate(headers):
        p.drawString(50 + i * 120, y, header)  # Reduce the x-coordinate multiplier

    y -= 15  # Reduce the space between header and data

    for month in months:
        month_data = ProfitSummary.objects.filter(
            created_at__year=month.year,
            created_at__month=month.month
        ).aggregate(
            total_pendapatan_bersih=Sum('pendapatan_bersih'),
            total_pendapatan_kotor=Sum('pendapatan_kotor'),
            total_profit=Sum('profit')
        )

        month_name = timezone.datetime(month.year, month.month, 1).strftime("%B %Y")
        total_pendapatan_bersih = f"Rp {month_data['total_pendapatan_bersih'] or 0}"
        total_pendapatan_kotor = f"Rp {month_data['total_pendapatan_kotor'] or 0}"
        total_profit = f"Rp {month_data['total_profit'] or 0}"

        data = [month_name, total_pendapatan_bersih, total_pendapatan_kotor, total_profit]

        for i, value in enumerate(data):
            p.drawString(50 + i * 120, y, str(value))  # Adjust the x-coordinate

        y -= 15  # Reduce the space between data for each month

    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="monthly_totals.pdf"'
    return response




def generate_all_summaries_pdf(request):
    all_profit_summaries = ProfitSummary.objects.all()

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF object using the BytesIO buffer
    p = canvas.Canvas(buffer, pagesize=letter)

    # Define the PDF content
    p.drawString(50, 750, "All Profit Summaries")
    y = 720  # Initial Y-coordinate

    # Set headers
    headers = ["Menu", "Pendapatan Bersih", "Pendapatan Kotor", "Profit", "Tanggal"]
    for i, header in enumerate(headers):
        p.drawString(50 + i * 120, y, header)

    y -= 20  # Move to the next line

    # Loop through all profit summaries and add content to the PDF
    for summary in all_profit_summaries:
        menu = summary.menu.nama_menu_lengkap
        pendapatan_bersih = summary.pendapatan_bersih
        pendapatan_kotor = summary.pendapatan_kotor
        profit = summary.profit
        tanggal = summary.created_at.strftime("%d-%m-%Y")  # Format the date

        data = [menu, pendapatan_bersih, pendapatan_kotor, profit, tanggal]

        for i, value in enumerate(data):
            p.drawString(50 + i * 120, y, str(value))

        y -= 20  # Move to the next line

    # Save and close the PDF
    p.save()

    # Generate the response to send the PDF
    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_profit_summaries.pdf"'
    return response





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
            data_menu.save()  

            harga_menu = HargaMenu.objects.create(menu=data_menu, size=jenis_size, harga_menu=harga_menu_value)

            return redirect(add_data_menu) 
    else:
        form = DataMenuForm()

    return render(request, 'admin/tambahMenu.html', {'form': form})

def edit_menu(request, id):
    data_menu = get_object_or_404(DataMenu, id=id)
    if request.method == 'POST':
        form = DataMenuEditForm(request.POST, instance=data_menu)
        if form.is_valid():
            form.save()
            return redirect('menu_view') 
    else:
        form = DataMenuEditForm(instance=data_menu)
    return render(request, 'admin/editMenu.html', {'form': form, 'data_menu': data_menu})

def hapus_menu(request, id):
    data_menu = get_object_or_404(DataMenu, id=id)
    if request.method == 'POST':
        data_menu.delete()
        return redirect('menu_view')  
    return render(request, 'admin/hapusMenu.html', {'data_menu': data_menu})

def delete_price(request, menu_id, price_id):
    menu = get_object_or_404(DataMenu, pk=menu_id)
    price = get_object_or_404(HargaMenu, pk=price_id)

    if request.method == 'POST':
        price.delete()
        return redirect(menu_view)
    return render(request, menu_view, {'menu': menu})

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

def profit_summary_of_month(request, year, month):
    # Convert year and month to integers
    year = int(year)
    month = int(month)
    
    # Fetch the profit summary for the given year and month
    profit_summary = ProfitSummary.objects.filter(
        created_at__year=year,
        created_at__month=month
    )

    return render(request, 'Admin/profit_summary_of_month.html', {
        'profit_summary': profit_summary,
        'year': year,
        'month': month,
    })


#bahan menu

def bahan_menu_list(request):
    all_bahanmenu = BahanMenu.objects.all()
    return render(request, 'bahan/bahan.html', {'all_bahanmenu': all_bahanmenu})
def add_ingredient(request):
    if request.method == 'POST':
        form = BahanMenuForm(request.POST)
        if form.is_valid():
            bahan_menu = form.save(commit=False)
            bahan_menu.menu_id = request.POST.get('menu') 
            bahan_menu.size_id = request.POST.get('size')  
            bahan_menu.save()
            return redirect('bahan_menu_list')  
    else:
        form = BahanMenuForm()

    return render(request, 'bahan/tambahBahan.html', {'form': form})

def edit_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(BahanMenu, pk=ingredient_id)

    if request.method == 'POST':
        form = BahanMenuForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect(bahan_menu_list)  
    else:
        form = BahanMenuForm(instance=ingredient)

    return render(request, 'bahan/editBahan.html', {'form': form, 'ingredient': ingredient})

def delete_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(BahanMenu, pk=ingredient_id)
    menu_id = ingredient.menu.id
    
    if request.method == 'POST':
        ingredient.delete()
        return redirect(bahan_menu_list)

    return render(request, 'bahan/hapusBahan.html', {'ingredient': ingredient})

