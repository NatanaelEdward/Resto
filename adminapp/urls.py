from django.urls import path
from .views import generate_monthly_totals_pdf,generate_all_summaries_pdf,generate_monthly_pdf,laporanAdmin,add_data_menu,menu_view,edit_menu,hapus_menu,update_price,add_ingredient,edit_ingredient,delete_ingredient,bahan_menu_list,delete_price,profit_summary_of_month,add_jenis_menu,add_kelompok_menu,edit_jenis_menu,edit_kelompok_menu,delete_jenis_menu,delete_kelompok_menu

urlpatterns =[
    path('menuAdmin/',menu_view,name='menu_view'),    
    #Admin
    path('menu/list/',bahan_menu_list,name='bahan_menu_list'),
    path('laporanAdmin/', laporanAdmin,name='laporanAdmin'),
    path('tambahMenu/', add_data_menu, name='tambahMenu'),
    path('menu/edit/<int:id>/', edit_menu, name='edit_menu'),
    
    path('generate_monthly_pdf/<int:year>/<int:month>/', generate_monthly_pdf, name='generate_monthly_pdf'),
    path('generate_all_summaries_pdf/', generate_all_summaries_pdf, name='generate_all_summaries_pdf'),
    path('generate_all_monthly_total_pdf/', generate_monthly_totals_pdf, name='generate_monthly_totals_pdf'),

    path('profit_summary_of_month/<int:year>/<int:month>/', profit_summary_of_month, name='profit_summary_of_month'),

    path('menu/delete/<int:id>/', hapus_menu, name='hapus_menu'),
    path('menu/editprice/<int:id>/', update_price, name='update_price'),
    path('menu/add_ingredient/', add_ingredient, name='add_ingredient'),
    path('menu/<int:menu_id>/price/<int:price_id>/delete/', delete_price, name='delete_price'),
    path('menu/edit_ingredient/<int:ingredient_id>/', edit_ingredient, name='edit_ingredient'),
    path('menu/delete_ingredient/<int:ingredient_id>/', delete_ingredient, name='delete_ingredient'),

    path('add_jenis_menu/', add_jenis_menu, name='tambahJenis'),
    path('edit_jenis_menu/<int:jenis_menu_id>/', edit_jenis_menu, name='editJenis'),
    path('delete_jenis_menu/<int:jenis_menu_id>/', delete_jenis_menu, name='hapusJenis'),

    path('menu/add_kelompok_menu/', add_kelompok_menu, name='tambahKelompok'),
    path('menu/edit_kelompok_menu/<int:kelompok_menu_id>/', edit_kelompok_menu, name='editKelompok'),
    path('menu/delete_kelompok_menu/<int:kelompok_menu_id>/', delete_kelompok_menu, name='hapusKelompok'),

    path('menu/add_jenis_menu/',add_jenis_menu, name='tambahJenis'),
    path('menu/edit_jenis_menu/<int:jenis_menu_id>/', edit_jenis_menu, name='editJenis'),
    path('menu/delete_jenis_menu/<int:jenis_menu_id>/',delete_jenis_menu,name='hapusJenis')
    ]


