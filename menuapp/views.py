# menuapp/views.py
import json
import random, string
from django.shortcuts import render, redirect
from .forms import DataMenuForm
from django.db.models import F

from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum
from django.db import transaction
from .models import DataMenu, JenisMenu,PenjualanDetail,HargaMenu,JenisSize,CartItem,PenjualanFaktur,InvoiceSequence
from decimal import Decimal

def index_makanan(request):
    kategori = request.GET.get('kategori', '')  # Mendapatkan nilai parameter kategori dari URL

    # Check if a category was specified
    if kategori:
        menus = DataMenu.objects.filter(jenis_menu__nama_jenis=kategori).prefetch_related('hargamenu_set__size')
    else:
        # If no category is specified, retrieve all menus
        menus = DataMenu.objects.all().prefetch_related('hargamenu_set__size')

    return render(request, 'user/indexMakanan.html', {'menus': menus, 'kategori': kategori})


def checkout_success(request):

    return render(request, 'user/checkout_success.html')

def index_minuman(request):
    kategori = request.GET.get('kategori', '')  # Mendapatkan nilai parameter kategori dari URL
    menus = DataMenu.objects.filter(jenis_menu__nama_jenis=kategori)

    return render(request, 'user/indexMinuman.html', {'menus': menus, 'kategori': kategori})

def index_dessert(request):
    kategori = request.GET.get('kategori', '')  # Mendapatkan nilai parameter kategori dari URL
    menus = DataMenu.objects.filter(jenis_menu__nama_jenis=kategori)

    return render(request, 'user/indexDessert.html', {'menus': menus, 'kategori': kategori})

def index_snack(request):
    kategori = request.GET.get('kategori', '')  # Mendapatkan nilai parameter kategori dari URL
    menus = DataMenu.objects.filter(jenis_menu__nama_jenis=kategori)

    return render(request, 'user/indexSnack.html', {'menus': menus, 'kategori': kategori})

def tambah_menu(request):
    if request.method == 'POST':
        form = DataMenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tambah_menu')  # Ganti 'daftar_menu' dengan nama URL daftar menu Anda.
    else:
        form = DataMenuForm()
    return render(request, 'Admin/tambahMenu.html', {'form': form})

def add_to_cart(request, menu_id, size_id, qty):
    menu = DataMenu.objects.get(pk=menu_id)
    size = JenisSize.objects.get(pk=size_id)
    user = request.user
    
    # Ensure qty is greater than 0 before creating or updating the cart item
    qty = int(qty)
    if qty > 0:
        cart_item, created = CartItem.objects.get_or_create(user=user, menu=menu, size=size)
        cart_item.qty = qty
        cart_item.save()
    else:
        # Remove the cart item if qty is 0
        CartItem.objects.filter(user=user, menu=menu, size=size).delete()
    
    return redirect('index_makanan')


def generate_invoice_number(prefix, nomor_meja):
    today = timezone.now()
    date_part = today.strftime("%Y%m%d")  # Get today's date as "YYYYMMDD"

    with transaction.atomic():
        # Fetch the current sequence number for the given nomor_meja and update it
        invoice_sequence, created = InvoiceSequence.objects.get_or_create(nomor_meja=nomor_meja)
        if prefix == 'N':
            invoice_number = f"{prefix}{nomor_meja}_{date_part}_{invoice_sequence.nota_sequence:04d}"
            InvoiceSequence.objects.filter(pk=invoice_sequence.pk).update(nota_sequence=F('nota_sequence') + 1)
        elif prefix == 'F':
            invoice_number = f"{prefix}{nomor_meja}_{date_part}_{invoice_sequence.faktur_sequence:04d}"
            InvoiceSequence.objects.filter(pk=invoice_sequence.pk).update(faktur_sequence=F('faktur_sequence') + 1)

    return invoice_number



def checkout(request):
    user = request.user
    user_profile = request.user.userprofile
    data_meja = user_profile.data_meja
    cart_items = CartItem.objects.filter(user=user)
    harga_tiap_menu = [float(item.menu.hargamenu_set.get(size=item.size).harga_menu) for item in cart_items]
    total_tiap_menu = [float(item.menu.hargamenu_set.get(size=item.size).harga_menu * item.qty) for item in cart_items]
    total_amount = sum(item.menu.hargamenu_set.get(size=item.size).harga_menu * item.qty for item in cart_items)
    nomor_meja = data_meja.nomor_meja
    # ini untuk mengengetahui jika di post akan terhapus
    if request.method == 'POST':
        with transaction.atomic():
            nomor_nota_penjualan = generate_invoice_number('N', nomor_meja)
            
            for cart_item in cart_items:
                harga_menu = HargaMenu.objects.get(menu=cart_item.menu, size=cart_item.size)
                jumlah_harga = harga_menu.harga_menu * cart_item.qty
                PenjualanDetail.objects.create(
                    nomor_nota_penjualan=nomor_nota_penjualan,
                    kode_menu=cart_item.menu,
                    harga_menu=harga_menu.harga_menu,
                    jumlah_harga=jumlah_harga,
                    qty_menu=cart_item.qty
                )
                cart_item.delete()  # Hapus item dari keranjang belanja setelah berhasil checkout
            
            # Calculate total_penjualan from PenjualanDetail
            total_penjualan = PenjualanDetail.objects.filter(nomor_nota_penjualan=nomor_nota_penjualan).aggregate(
                total_penjualan=Sum('jumlah_harga')
            )['total_penjualan'] or 0

            # Get the input pembayaran (you can retrieve it from your form or any other method)
            pembayaran = Decimal(request.POST.get('pembayaran', 0))  # Replace with the actual input field name
            
            # Calculate kembalian, set to 0 if pembayaran is zero or None
            kembalian = total_penjualan - pembayaran if pembayaran is not None and pembayaran != 0 else 0

            # Create PenjualanFaktur instance
            PenjualanFaktur.objects.create(
                kode_penjualan_faktur=generate_invoice_number('F', nomor_meja),
                nomor_nota_penjualan=nomor_nota_penjualan,
                nomor_meja=nomor_meja,  # You can set this based on cashier input
                cara_pembayaran="",  # You can set this based on cashier input
                status_lunas=False,  # You can set this based on cashier input
                jenis_pembayaran="",  # You can set this based on cashier input
                total_penjualan=total_penjualan,
                pembayaran=pembayaran,  # Use the input value
                kembalian=kembalian,  # Calculate kembalian
            )

            return redirect('index_makanan')
    else:
        return render(request, 'user/checkout_page.html', {'cart_items': cart_items, 'total_amount': total_amount, 'total_tiap_menu': total_tiap_menu, 'harga_tiap_menu': harga_tiap_menu})





def get_cart_items(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user).select_related('menu', 'size')

    # Serialize cart items as JSON data
    cart_data = [
        {
            'menu_id': item.menu.id,
            'size_id' : item.size.id,
            'menu_name': item.menu.nama_menu_lengkap,
            'size': item.size.nama_size,
            'qty': item.qty,
            'menu_image': item.menu.gambar_menu.url,
        }
        for item in cart_items
    ]

    return JsonResponse({'cart_items': cart_data})

def remove_from_cart(request, menu_id, size_id):
    menu = DataMenu.objects.get(pk=menu_id)
    size = JenisSize.objects.get(pk=size_id)
    user = request.user
    
    # Remove the cart item
    CartItem.objects.filter(user=user, menu=menu, size=size).delete()
    
    return JsonResponse({'message': 'Item removed from the cart.'})

