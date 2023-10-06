from django.db import models

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
    nomor_nota_penjualan = models.CharField(max_length=20, primary_key=True)
    kode_menu = models.ForeignKey(DataMenu, on_delete=models.CASCADE)
    harga_menu = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah_harga = models.DecimalField(max_digits=10, decimal_places=2)
    qty_menu = models.PositiveIntegerField()

    def __str__(self):
        return self.nomor_nota_penjualan