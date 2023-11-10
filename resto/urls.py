"""
URL configuration for resto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404,handler500,handler403
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    path('',include('adminapp.urls')),
    path('',include('kasirapp.urls')),
    path('',include('menuapp.urls')),
]

handler404 = views.err404
handler500 = views.err500
handler403 = views.err403

handler404 = 'app.views.err404'
handler500 = 'app.views.err500'
handler403 = 'app.views.err403'

def err404(request, exception):
    return views.login_view(request)

def err500(request):
    return views.login_view(request)

def err403(request):
    return views.login_view(request)
