from django.urls import path
from .views import Login,index

urlpatterns =[
    path('Login', Login, name='Login'),
    path('index', index,name='index'), 
]