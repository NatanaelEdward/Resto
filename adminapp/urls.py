from django.urls import path
from .views import tambahMenu,editMenu,hapusMenu,laporanAdmin

urlpatterns =[
    
    #Admin
    path('laporanAdmin/', laporanAdmin,name='laporanAdmin'),
    path('tambahMenu/', tambahMenu, name='tambahMenu'),
    path('editMenu/', editMenu, name='editMenu'),
    path('hapusMenu/', hapusMenu, name='hapusMenu'),
    ]