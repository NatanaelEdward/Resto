from django.urls import path
from .views import login_view,indexKasir,indexAdmin,logout_view

urlpatterns =[
    path('', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('indexKasir', indexKasir,name='indexKasir'),
    path('indexAdmin', indexAdmin,name='indexAdmin'),
]