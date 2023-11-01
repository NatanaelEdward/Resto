# menuapp/forms.py
from django import forms
from .models import DataMenu,PenjualanFaktur,BahanMenu,JenisSize,KelompokMenu,JenisMenu,HargaMenu

class DataMenuForm(forms.ModelForm):
    class Meta:
        model = DataMenu
        fields = ['kode_menu', 'nama_menu_lengkap', 'nama_menu_singkat', 'jenis_menu', 'gambar_menu', 'keterangan_menu', 'status_aktif_menu']
        
    kelompok_menu = forms.ModelChoiceField(queryset=KelompokMenu.objects.all())
    jenis_menu = forms.ModelChoiceField(queryset=JenisMenu.objects.all())
    jenis_size = forms.ModelChoiceField(queryset=JenisSize.objects.all())
    harga_menu = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(DataMenuForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            jenis_size = kwargs['instance'].jenis_size
            if jenis_size:
                self.fields['jenis_size'].queryset = JenisSize.objects.filter(size=jenis_size)
            else:
                self.fields['jenis_size'].queryset = JenisSize.objects.none()

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

class BahanMenuForm(forms.ModelForm):
    class Meta:
        model = BahanMenu
        fields = ['name', 'price', 'qty', 'menu', 'size']