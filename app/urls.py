from django.urls import path
from .views import indexKasir,indexAdmin,logout_view,login_view, tambahMenu,editMenu,hapusMenu,laporanAdmin

urlpatterns =[
    path('', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),

    path('indexKasir', indexKasir,name='indexKasir'),
    path('indexAdmin', indexAdmin,name='indexAdmin'),
    path('laporanAdmin', laporanAdmin,name='laporanAdmin'),


    path('tambahMenu', tambahMenu, name='tambahMenu'),
    path('editMenu', editMenu, name='editMenu'),
    path('hapusMenu', hapusMenu, name='hapusMenu'),
]