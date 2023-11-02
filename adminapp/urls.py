from django.urls import path
from .views import laporanAdmin,add_data_menu,menu_view,edit_menu,hapus_menu,update_price,add_ingredient,edit_ingredient,delete_ingredient,bahan_menu_list,delete_price

urlpatterns =[
    path('menuAdmin/',menu_view,name='menu_view'),    
    #Admin
    path('menu/list/',bahan_menu_list,name='bahan_menu_list'),
    path('laporanAdmin/', laporanAdmin,name='laporanAdmin'),
    path('tambahMenu/', add_data_menu, name='tambahMenu'),
    path('menu/edit/<int:id>/', edit_menu, name='edit_menu'),
    path('menu/delete/<int:id>/', hapus_menu, name='hapus_menu'),
    path('menu/editprice/<int:id>/', update_price, name='update_price'),
    path('menu/add_ingredient/', add_ingredient, name='add_ingredient'),
    path('menu/<int:menu_id>/price/<int:price_id>/delete/', delete_price, name='delete_price'),
    path('menu/edit_ingredient/<int:ingredient_id>/', edit_ingredient, name='edit_ingredient'),
    path('menu/delete_ingredient/<int:ingredient_id>/', delete_ingredient, name='delete_ingredient'),
    ]