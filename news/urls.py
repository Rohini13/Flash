from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('readAloud/', views.readAloud, name='readAloud'),
    path('stop/', views.stop, name='stop'),
]