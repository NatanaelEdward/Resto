from django.urls import path
from .views import kasiran,pesanan,tabelKasir,update_order,cancel_order,delete_order,generate_pdf

urlpatterns = [
    path('kasiran', kasiran, name='kasiran'),
    path('pesanan', pesanan, name='pesanan'),
    path('tabelKasir', tabelKasir, name='tabelKasir'),
    path('update_order/<int:order_id>/',update_order, name='update_order'),
    path('cancel_order/<int:order_id>/',cancel_order, name='cancel_order'),
    path('delete_order/<int:order_id>/',delete_order, name='delete_order'),
    path('generate_pdf/<int:order_id>/',generate_pdf, name='generate_pdf'),


]
