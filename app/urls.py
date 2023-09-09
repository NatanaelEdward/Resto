from django.urls import path
from .views import login_view,index,logout_view

urlpatterns =[
    path('', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('index', index,name='index'), 
]