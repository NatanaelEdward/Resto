# menuapp/views.py
import json
import random, string
from django.shortcuts import render, redirect,get_object_or_404
from .forms import DataMenuForm,BahanMenuForm  
from django.db.models import F,ExpressionWrapper, DecimalField
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum
from django.db import transaction
from .models import DataMenu, JenisMenu,PenjualanDetail,HargaMenu,JenisSize,CartItem,PenjualanFaktur,InvoiceSequence,KelompokMenu,BahanMenu,ProfitSummary
from decimal import Decimal
from django.contrib.auth.decorators import login_required

@login_required
def index_makanan(request):
    kelompok_makanan = KelompokMenu.objects.get(nama_kelompok="makanan")
    
    # Get the 'kategori' parameter from the request
    kategori = request.GET.get('kategori')

    # Filter menus based on the 'jenis_menu' attribute
    if kategori:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_makanan, jenis_menu__nama_jenis=kategori)
    else:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_makanan)
    
    return render(request, 'user/indexMakanan.html', {'menus': menus, 'kategori': 'makanan'})

@login_required
def index_minuman(request):
    kelompok_minuman = KelompokMenu.objects.get(nama_kelompok="minuman")
    
    # Get the 'kategori' parameter from the request
    kategori = request.GET.get('kategori')

    # Filter menus based on the 'jenis_menu' attribute
    if kategori:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_minuman, jenis_menu__nama_jenis=kategori)
    else:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_minuman)
    
    return render(request, 'user/indexminuman.html', {'menus': menus, 'kategori': 'makanan'})

@login_required
def index_dessert(request):
    kelompok_dessert = KelompokMenu.objects.get(nama_kelompok="dessert")
    
    # Get the 'kategori' parameter from the request
    kategori = request.GET.get('kategori')

    # Filter menus based on the 'jenis_menu' attribute
    if kategori:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_dessert, jenis_menu__nama_jenis=kategori)
    else:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_dessert)
    
    return render(request, 'user/indexdessert.html', {'menus': menus, 'kategori': 'makanan'})

@login_required
def index_snack(request):
    kelompok_snack= KelompokMenu.objects.get(nama_kelompok="snack")
    
    # Get the 'kategori' parameter from the request
    kategori = request.GET.get('kategori')

    # Filter menus based on the 'jenis_menu' attribute
    if kategori:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_snack, jenis_menu__nama_jenis=kategori)
    else:
        menus = DataMenu.objects.filter(jenis_menu__kelompok_menu=kelompok_snack)
    
    return render(request, 'user/indexsnack.html', {'menus': menus, 'kategori': 'makanan'})

@login_required
def checkout_success(request):

    return render(request, 'user/checkout_success.html')

@login_required
def tambah_menu(request):
    if request.method == 'POST':
        form = DataMenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tambah_menu')  # Ganti 'daftar_menu' dengan nama URL daftar menu Anda.
    else:
        form = DataMenuForm()
    return render(request, 'Admin/tambahMenu.html', {'form': form})

@login_required
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

@login_required
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

@login_required
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
            'menu_price': item.menu.hargamenu_set.get(size=item.size).harga_menu,
            'menu_image': item.menu.gambar_menu.url,
        }
        for item in cart_items
    ]

    return JsonResponse({'cart_items': cart_data})

@login_required
def remove_from_cart(request, menu_id, size_id):
    menu = DataMenu.objects.get(pk=menu_id)
    size = JenisSize.objects.get(pk=size_id)
    user = request.user
    
    # Remove the cart item
    CartItem.objects.filter(user=user, menu=menu, size=size).delete()
    
    return JsonResponse({'message': 'Item removed from the cart.'})

@login_required
def add_bahan_menu(request, menu_id):
    menu = get_object_or_404(DataMenu, pk=menu_id)
    sizes = JenisSize.objects.all()  # Get available sizes, adjust query as needed

    if request.method == 'POST':
        form = BahanMenuForm(request.POST)
        if form.is_valid():
            bahan = form.save(commit=False)
            bahan.menu = menu
            bahan.save()
            return redirect(add_bahan_menu, menu_id=menu_id)  # Redirect to menu detail or desired page
    else:
        form = BahanMenuForm()

    return render(request, 'admin/bahanMenu.html', {'form': form, 'menu': menu, 'sizes': sizes})

@login_required
def menu_detail(request, menu_id,size_id):
    menu = DataMenu.objects.get(pk=menu_id)
    menu_prices = HargaMenu.objects.filter(menu=menu)
    ingredients_with_prices = BahanMenu.objects.filter(menu=menu)

    penjualan_details = PenjualanDetail.objects.filter(kode_menu=menu)
    total_bersih = 0

    for detail in penjualan_details:
        bahan_details = BahanMenu.objects.filter(menu=menu,size=size_id)
        total_bersih += sum(
            bahan.price * detail.qty_menu for bahan in bahan_details
        )

    # Calculate pendapatan_kotor for the menu
    total_kotor = sum(detail.jumlah_harga for detail in penjualan_details)

    # Calculate profit for the menu
    total_profit = total_bersih - total_kotor

    # Create and save ProfitSummary for the menu
    profit_summary, created = ProfitSummary.objects.get_or_create(
        menu=menu,
        defaults={
            'pendapatan_bersih': total_bersih,
            'pendapatan_kotor': total_kotor,
            'profit': total_profit
        }
    )

    return render(request, 'admin/menu_detail.html', {
        'menu': menu,
        'menu_prices': menu_prices,
        'ingredients_with_prices': ingredients_with_prices,
        'profit_summary': profit_summary
    })

