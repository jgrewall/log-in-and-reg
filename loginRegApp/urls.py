from django.urls import path
from . import views

urlpatterns =[
    #display
    path('', views.index),
    path('dashboard', views.displaydashboard),

    #redirect
    path('newUser', views.newUser),
    path('login', views.login),
    path('logout', views.logout)
]