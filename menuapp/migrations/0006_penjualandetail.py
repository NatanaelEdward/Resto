# Generated by Django 4.2.4 on 2023-10-08 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0005_delete_penjualandetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='PenjualanDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor_nota_penjualan', models.CharField(max_length=20)),
                ('harga_menu', models.DecimalField(decimal_places=2, max_digits=10)),
                ('jumlah_harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qty_menu', models.PositiveIntegerField()),
                ('kode_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menuapp.datamenu')),
            ],
        ),
    ]
