from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('readAloud/', views.readAloud, name='readAloud'),
    path('stop/', views.stop, name='stop'),
    path('signin/', views.signIn),
    path('postsign/', views.postsign),
    path('logout/', views.logout, name="log"),
    path('signup/', views.signUp, name="signup"),
    path('postsignup/', views.postsignup, name="postsignup")
]
