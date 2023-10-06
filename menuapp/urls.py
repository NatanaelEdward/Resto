# menuapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('tambah_menu/', views.tambah_menu, name='tambah_menu'),
    path('indexMakanan/', views.index_makanan, name='index_makanan'),
    path('indexMinuman/', views.index_minuman, name='index_minuman'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
