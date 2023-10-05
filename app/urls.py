from django.urls import path
from .views import indexKasir,indexAdmin,indexUser,logout_view,login_view, tambahMenu,editMenu,hapusMenu,laporanAdmin,kasiran,pesanan,tabelKasir,indexMakanan,indexDessert,indexMinuman,indexSnack
from . import views

urlpatterns =[
    path('api/categories/', views.get_categories, name='categories'),
    path('', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),

    #index
    path('indexKasir', indexKasir,name='indexKasir'),
    path('indexAdmin', indexAdmin,name='indexAdmin'),
    path('indexUser', indexUser, name='indexUser'),
    
    #Admin
    path('laporanAdmin', laporanAdmin,name='laporanAdmin'),
    path('tambahMenu', tambahMenu, name='tambahMenu'),
    path('editMenu', editMenu, name='editMenu'),
    path('hapusMenu', hapusMenu, name='hapusMenu'),

    #kasir
    path('kasiran', kasiran, name='kasiran'),
    path('pesanan', pesanan, name='pesanan'),
    path('tabelKasir', tabelKasir, name='tabelKasir'),

    #user
    path('indexMakanan', indexMakanan, name='indexMakanan'),
    path('indexMinuman', indexMinuman, name='indexMinuman'),
    path('indexDessert', indexDessert, name='indexDessert'),
    path('indexSnack', indexSnack, name='indexSnack'),
    ]

    