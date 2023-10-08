# menuapp/views.py
import json
import random, string
from django.shortcuts import render, redirect
from .forms import DataMenuForm
from django.http import JsonResponse
from django.db import transaction
from .models import DataMenu, JenisMenu,PenjualanDetail,HargaMenu,JenisSize,CartItem
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


def generate_random_invoice_number():
    while True:
        characters = string.ascii_letters + string.digits
        invoice_number = ''.join(random.choice(characters) for _ in range(10))
        
        # Periksa apakah nomor nota penjualan sudah ada di database
        if not PenjualanDetail.objects.filter(nomor_nota_penjualan=invoice_number).exists():
            return invoice_number



def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    harga_tiap_menu = [float(item.menu.hargamenu_set.get(size=item.size).harga_menu) for item in cart_items]
    total_tiap_menu = [float(item.menu.hargamenu_set.get(size=item.size).harga_menu * item.qty) for item in cart_items]
    total_amount = sum(item.menu.hargamenu_set.get(size=item.size).harga_menu * item.qty for item in cart_items)

    if request.method == 'POST':
        
        with transaction.atomic():
            nomor_nota_penjualan = generate_random_invoice_number()  # Buat nomor nota penjualan acak
            
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
            
            return redirect('index_makanan')
    else:
        return render(request, 'user/checkout_page.html', {'cart_items': cart_items, 'total_amount': total_amount, 'total_tiap_menu' : total_tiap_menu, 'harga_tiap_menu' : harga_tiap_menu})

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

