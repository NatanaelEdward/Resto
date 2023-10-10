from django.core.management.base import BaseCommand
from menuapp.models import KelompokMenu, JenisMenu, JenisSize, DataMenu, HargaMenu, PenjualanFaktur

def seed_data():
    # Create KelompokMenu instances
    kelompok_makanan, created = KelompokMenu.objects.get_or_create(
        kode_kelompok='MAKANAN',
        nama_kelompok='Makanan'
    )

    # Create JenisMenu instances
    jenis_ayambakar, created = JenisMenu.objects.get_or_create(
        kode_jenis='M',
        nama_jenis='Meat',
        kelompok_menu=kelompok_makanan
    )

    # Create JenisSize instances
    size_small, created = JenisSize.objects.get_or_create(
        kode_size='S',
        nama_size='Small'
    )

    # Create DataMenu instances
    menu1, created = DataMenu.objects.get_or_create(
        kode_menu='M1',
        nama_menu_lengkap='Ayam Bakar',
        nama_menu_singkat='AYMBKR',
        jenis_menu=jenis_ayambakar,
        gambar_menu='menu_images/ayam_bakar.jpeg',
        keterangan_menu='Ayam Tapi Di Bakar',
        status_aktif_menu=True,
    )

    # Create HargaMenu instances
    harga_menu1, created = HargaMenu.objects.get_or_create(
        menu=menu1,
        size=size_small,
        harga_menu=10.99
    )

    # Create PenjualanFaktur instances
    faktur1, created = PenjualanFaktur.objects.get_or_create(
        kode_penjualan_faktur='F1',
        nomor_nota_penjualan='N1',
        nomor_meja='M1',
        cara_pembayaran='Cash',
        jenis_pembayaran='Tunai',
        total_penjualan=10.99,
        pembayaran=20.0,
        kembalian=9.01
    )

class Command(BaseCommand):
    help = 'Seed initial data into database'

    def handle(self, *args, **kwargs):
        seed_data()
        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
