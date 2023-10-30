from django.urls import path
from .views import indexKasir,indexUser,logout_view,login_view,indexAdmin
from . import views

urlpatterns =[
    path('api/categories/', views.get_categories, name='categories'),
    path('', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),

    #index
    path('indexAdmin', indexAdmin,name='indexAdmin'),
    path('indexKasir', indexKasir,name='indexKasir'),
    path('indexUser', indexUser, name='indexUser'),
    
    ]

    