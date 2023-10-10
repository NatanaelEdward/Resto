from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from menuapp.models import PenjualanDetail,PenjualanFaktur
from django.contrib.auth.decorators import login_required
import requests
from decimal import Decimal
from django.http import JsonResponse

# Create your views here.

@login_required
def kasiran(request):
     if request.user.userprofile.role != 'kasir':
            
            return redirect('login_view')
     return render(request, 'Kasir/kasiran.html')

@login_required
def pesanan(request):
    if request.user.userprofile.role != 'kasir':
        return redirect('login_view')

    # Retrieve both completed and pending PenjualanFaktur instances
    completed_orders = PenjualanFaktur.objects.filter(status_lunas=True)
    pending_orders = PenjualanFaktur.objects.filter(status_lunas=False)

    context = {
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'kasir/pesanan.html', context)

@login_required
def tabelKasir(request):
     if request.user.userprofile.role != 'kasir':
            return redirect('login_view')
     return render(request, 'kasir/tabelKasir.html')

@login_required
def update_order(request, order_id):
    if request.user.userprofile.role != 'kasir':
        return redirect('login_view')

    # Get the PenjualanFaktur instance to update
    order = get_object_or_404(PenjualanFaktur, id=order_id)

    if request.method == 'POST':
        # Get the data from the form
        pembayaran = Decimal(request.POST.get('pembayaran', 0))
        
        # Calculate kembalian (ensure it's positive)
        kembalian = order.total_penjualan - pembayaran
        order.kembalian = abs(kembalian)  # Use abs() to make it positive
        
        # Update the order data
        order.pembayaran = pembayaran
        order.status_lunas = 1
        
        # Save the changes
        order.save()

        # Redirect back to the "pesanan" page or any other desired page
        return redirect('pesanan')

    # Handle GET request or any other logic if needed
    return render(request, 'kasir/pesanan.html', {'order': order})



@login_required
def cancel_order(request, order_id):
     if request.user.userprofile.role != 'kasir':
        return redirect('login_view')
     
     order = get_object_or_404(PenjualanFaktur, id=order_id)

     if request.method == 'POST':
          
        order.status_lunas = 0

        order.save()

        return redirect('pesanan')
     return render(request, 'kasir/pesanan.html', {'order': order})

@login_required
def delete_order(request, order_id):
    if request.user.userprofile.role != 'kasir':
        return redirect('login_view')

    # Get the PenjualanFaktur instance to delete
    order = get_object_or_404(PenjualanFaktur, id=order_id)

    if request.method == 'POST':
        # Delete associated PenjualanDetail records
        PenjualanDetail.objects.filter(nomor_nota_penjualan=order.nomor_nota_penjualan).delete()
        
        # Delete the PenjualanFaktur (order) instance
        order.delete()

        # Redirect to a relevant page (e.g., pesanan or a confirmation page)
        return redirect('pesanan')

    # Handle GET request or any other logic if needed
    return render(request, 'kasir/pesanan.html', {'order': order})

     

