from django.urls import path
from .views import laporanAdmin,add_data_menu,menu_view,edit_menu,hapus_menu

urlpatterns =[
    path('menuAdmin/',menu_view,name='menu_view'),    
    #Admin
    path('laporanAdmin/', laporanAdmin,name='laporanAdmin'),
    path('tambahMenu/', add_data_menu, name='tambahMenu'),
    path('menu/edit/<int:id>/', edit_menu, name='edit_menu'),
    path('menu/delete/<int:id>/', hapus_menu, name='hapus_menu'),
    ]