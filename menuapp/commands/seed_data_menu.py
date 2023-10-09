import os
from django.core.management.base import BaseCommand
from django.core.files import File
from menuapp.models import DataMenu, JenisMenu, JenisSize, KelompokMenu

class Command(BaseCommand):
    help = 'Seed DataMenu with initial data'

    def handle(self, *args, **kwargs):
        # Create some JenisSize instances
        size_small, created = JenisSize.objects.get_or_create(
            kode_size='S',
            nama_size='Small'
        )

        size_medium, created = JenisSize.objects.get_or_create(
            kode_size='M',
            nama_size='Medium'
        )

        size_large, created = JenisSize.objects.get_or_create(
            kode_size='L',
            nama_size='Large'
        )

        kelompok_makanan, created = KelompokMenu.objects.get_or_create(
            kode_kelompok='MAKANAN',
            nama_kelompok='Makanan'
        )

        # Create some JenisMenu instances belonging to 'Makanan' KelompokMenu
        jenis_pizza, created = JenisMenu.objects.get_or_create(
            kode_jenis='PIZZA',
            nama_jenis='Pizza',
            kelompok_menu=kelompok_makanan
        )

        jenis_burger, created = JenisMenu.objects.get_or_create(
            kode_jenis='BURGER',
            nama_jenis='Burger',
            kelompok_menu=kelompok_makanan
        )

        # Define paths to your local menu images
        menu1_image_path = 'menu_images/nama_file.jpg'
        menu2_image_path = 'menu_images/nama_file.jpg'

        # Create DataMenu instances and attach local images
        menu1 = DataMenu.objects.create(
            kode_menu='M1',
            nama_menu_lengkap='Margherita Pizza',
            nama_menu_singkat='Margherita',
            jenis_menu=jenis_pizza,
            keterangan_menu='Delicious Margherita pizza',
            status_aktif_menu=True,
        )
        with open(menu1_image_path, 'rb') as img_file:
            menu1.gambar_menu.save(
                os.path.basename(menu1_image_path),
                File(img_file)
            )

        menu2 = DataMenu.objects.create(
            kode_menu='M2',
            nama_menu_lengkap='Cheeseburger',
            nama_menu_singkat='Cheeseburger',
            jenis_menu=jenis_burger,
            keterangan_menu='Classic cheeseburger',
            status_aktif_menu=True,
        )
        with open(menu2_image_path, 'rb') as img_file:
            menu2.gambar_menu.save(
                os.path.basename(menu2_image_path),
                File(img_file)
            )

        # You can continue to create more menu items as needed

        self.stdout.write(self.style.SUCCESS('Successfully seeded DataMenu data'))
