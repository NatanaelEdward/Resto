from django.urls import path
from .views import login_view,index

urlpatterns =[
    path('', login_view, name='login_view'),
    path('index', index,name='index'), 
]