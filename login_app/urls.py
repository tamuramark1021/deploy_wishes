from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), 
    path('register/', views.register),
    path('login/', views.login),
    path('successful_login', views.success), 
    path('logout', views.logout),
]