# menuapp/forms.py
from django import forms
from .models import DataMenu,PenjualanFaktur

class DataMenuForm(forms.ModelForm):
    class Meta:
        model = DataMenu
        fields = '__all__'  # Atau tentukan bidang apa saja yang ingin Anda tampilkan dalam form.

# forms.py (create a new forms.py file if you don't have one already)
class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = PenjualanFaktur
        fields = ['nomor_meja', 'cara_pembayaran', 'jenis_pembayaran', 'pembayaran']

    def clean_pembayaran(self):
        pembayaran = self.cleaned_data['pembayaran']
        total_penjualan = self.instance.total_penjualan
        if pembayaran < total_penjualan:
            raise forms.ValidationError("Pembayaran harus lebih besar atau sama dengan total penjualan.")
        return pembayaran
