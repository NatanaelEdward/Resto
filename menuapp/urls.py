# menuapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('tambah_menu/', views.tambah_menu, name='tambah_menu'),
    path('indexMakanan/', views.index_makanan, name='index_makanan'),
    path('indexMinuman/', views.index_minuman, name='index_minuman'),
    path('add_to_cart/<int:menu_id>/<int:size_id>/<int:qty>/', views.add_to_cart, name='add_to_cart'),
    path('checkout_success', views.checkout_success, name='checkout_success'),
    path('get_cart_items/', views.get_cart_items, name='get_cart_items'),
    path('remove_from_cart/<int:menu_id>/<int:size_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Tambahkan URL untuk halaman checkout
    path('checkout/', views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
