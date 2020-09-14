from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entertainment/',views.index2, name='index2'),
    path('business/',views.index3,name='index3'),
    path('sports/',views.index4,name='index4'),
    path('readAloud/', views.readAloud, name='readAloud'),
    path('stop/', views.stop, name='stop'),
]