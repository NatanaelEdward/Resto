from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from django.dispatch import receiver
from django.utils import timezone

class KelompokMenu(models.Model):
    kode_kelompok = models.CharField(max_length=10, unique=True)
    nama_kelompok = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_kelompok

class JenisMenu(models.Model):
    kode_jenis = models.CharField(max_length=10, unique=True)
    nama_jenis = models.CharField(max_length=255)
    kelompok_menu = models.ForeignKey(KelompokMenu, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama_jenis

class JenisSize(models.Model):
    kode_size = models.CharField(max_length=10, unique=True)
    nama_size = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_size

class DataMenu(models.Model):
    kode_menu = models.CharField(max_length=10, unique=True)
    nama_menu_lengkap = models.CharField(max_length=255)
    nama_menu_singkat = models.CharField(max_length=50)
    jenis_menu = models.ForeignKey(JenisMenu, on_delete=models.CASCADE)
    gambar_menu = models.ImageField(upload_to='menu_images/')
    keterangan_menu = models.TextField()
    status_aktif_menu = models.BooleanField(default=True)

    def calculate_profit(self):
        penjualan_details = PenjualanDetail.objects.filter(kode_menu=self)
        total_profit = 0

        for detail in penjualan_details:
            harga_total = detail.jumlah_harga
            bahan_details = BahanMenu.objects.filter(menu=self)
            bahan_total_cost = sum(bahan.price * detail.qty_menu for bahan in bahan_details)
            total_profit += harga_total - bahan_total_cost

        return total_profit
    
    @property
    def total_price_with_bahan(self, size):
        harga_menu = HargaMenu.objects.get(menu=self, size=size).harga_menu
        return harga_menu - self.calculate_total_bahan_price(size)

    def __str__(self):
        return self.nama_menu_lengkap  

class HargaMenu(models.Model):
    menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    size = models.ForeignKey(JenisSize, on_delete=models.CASCADE)
    harga_menu = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu} - {self.size} - {self.harga_menu}"

    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    size = models.ForeignKey(JenisSize, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)

# models.py

class PenjualanFaktur(models.Model):
    kode_penjualan_faktur = models.CharField(max_length=20, unique=True)
    nomor_nota_penjualan = models.CharField(max_length=20)
    nomor_meja = models.CharField(max_length=10)
    cara_pembayaran = models.CharField(max_length=50)
    status_lunas = models.BooleanField(default=False)
    jenis_pembayaran = models.CharField(max_length=50)
    tanggal_penjualan = models.DateTimeField(auto_now_add=True)
    total_penjualan = models.DecimalField(max_digits=10, decimal_places=2)
    pembayaran = models.DecimalField(max_digits=10, decimal_places=2)
    kembalian = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.kode_penjualan_faktur
    
class ProfitSummary(models.Model):
    menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    pendapatan_bersih = models.DecimalField(max_digits=10, decimal_places=2)
    pendapatan_kotor = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)  
    def __str__(self):
        return f"Profit Summary for {self.menu}"
    
class PenjualanDetail(models.Model):
    nomor_nota_penjualan = models.CharField(max_length=20)
    kode_menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    harga_menu = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah_harga = models.DecimalField(max_digits=10, decimal_places=2)
    qty_menu = models.PositiveIntegerField()
    faktur = models.ForeignKey(PenjualanFaktur, on_delete=models.CASCADE, null=True, blank=True)
    profit_summary = models.ForeignKey(ProfitSummary, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nomor_nota_penjualan

class DataMeja(models.Model):
    nomor_meja = models.CharField(max_length=10, unique=True)
    status_aktif_meja = models.BooleanField(default=True)
    keterangan_meja = models.TextField()
    kapasitas_meja = models.PositiveIntegerField()
    status_terpakai = models.BooleanField(default=False)

    def __str__(self):
        return self.nomor_meja
    
class InvoiceSequence(models.Model):
    nomor_meja = models.CharField(max_length=10, unique=True)
    nota_sequence = models.PositiveIntegerField(default=1)
    faktur_sequence = models.PositiveIntegerField(default=1)

class BahanMenu(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()  # Assuming qty is in grams
    menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    size = models.ForeignKey(JenisSize, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
        
def create_or_update_profit_summary(faktur):
    if faktur.pembayaran != 0:
        for detail in PenjualanDetail.objects.filter(faktur=faktur):
            menu = detail.kode_menu

            total_bersih = BahanMenu.objects.filter(menu=menu).aggregate(
                total=ExpressionWrapper(F('price') * F('qty'), output_field=DecimalField())
            )['total'] or 0

            total_kotor = PenjualanDetail.objects.filter(kode_menu=menu, faktur=faktur).aggregate(
                total_kotor=Sum('jumlah_harga')
            )['total_kotor'] or 0

            total_profit = total_kotor - total_bersih

            profit_summary, created = ProfitSummary.objects.update_or_create(
                menu=menu,
                defaults={
                    'pendapatan_bersih': total_bersih,
                    'pendapatan_kotor': total_kotor,
                    'profit': total_profit
                }
            )
