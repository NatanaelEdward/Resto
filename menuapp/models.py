from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.nama_menu_lengkap

class HargaMenu(models.Model):
    menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    size = models.ForeignKey(JenisSize, on_delete=models.CASCADE)
    harga_menu = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu} - {self.size} - {self.harga_menu}"

class PenjualanDetail(models.Model):
    nomor_nota_penjualan = models.CharField(max_length=20)
    kode_menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    harga_menu = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah_harga = models.DecimalField(max_digits=10, decimal_places=2)
    qty_menu = models.PositiveIntegerField()

    def __str__(self):
        return self.nomor_nota_penjualan
    
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