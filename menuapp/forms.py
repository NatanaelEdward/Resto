# menuapp/forms.py
from django import forms
from .models import DataMenu

class DataMenuForm(forms.ModelForm):
    class Meta:
        model = DataMenu
        fields = '__all__'  # Atau tentukan bidang apa saja yang ingin Anda tampilkan dalam form.
