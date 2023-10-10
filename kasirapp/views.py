from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from menuapp.models import PenjualanDetail,PenjualanFaktur
from django.contrib.auth.decorators import login_required
import requests
from decimal import Decimal
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def generate_pdf(request, order_id):
    # Get the PenjualanFaktur instance
    order = get_object_or_404(PenjualanFaktur, id=order_id)

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=landscape(letter))

    # Set a large enough page size
    width, height = landscape(letter)
    p.setPageSize((width, height))

    # Define content to print
    content = [
        f'FAKTUR PENJUALAN',
        f'Nomor Nota Penjualan: {order.kode_penjualan_faktur}',
        f'Meja: {order.nomor_meja}',
        f'Tanggal Penjualan: {order.tanggal_penjualan.strftime("%b. %d, %Y, %I:%M %p")}',
        f'Total Penjualan: {order.total_penjualan}',
        f'Total Pembayaran : {order.pembayaran}',
        f'Kembalian : {order.kembalian}',
        f'Status Lunas : {"Lunas" if order.status_lunas else "Belum Lunas"}'
    ]

    # Set the Y-coordinate for the first line of content
    y = height - 100

    # Add content to the PDF
    for line in content:
        p.drawString(100, y, line)
        y -= 20  # Adjust the Y-coordinate for the next line

    # Close the PDF object cleanly and finalize the buffer.
    p.showPage()
    p.save()

    # FileResponse to send the PDF as a response
    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.kode_penjualan_faktur}.pdf"'
    response.write(pdf_data)

    return response




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

     

