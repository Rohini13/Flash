from django.urls import path
from . import views

urlpatterns = [
    path('', views.loading, name='loading'),
    path('main/', views.index, name='index'),
    path('world/',views.index1, name='index1'),
    path('local/',views.index2, name='index2'),
    path('science/',views.index3, name='index3'),
    path('economy/',views.index4, name='index4'),
    path('health/',views.index5,name='index5'),
    path('sports/',views.index6,name='index6'),
    path('entertainment/',views.index7,name='index7'),
    path('readAloud/', views.readAloud, name='readAloud'),
    path('stop/', views.stop, name='stop'),
    path('signin/', views.signIn),
    path('postsign/', views.postsign),
    path('logout/', views.logout, name="log"),
    path('signup/', views.signUp, name="signup"),
    path('postsignup/', views.postsignup, name="postsignup"),
    path('/details/<int:newsid>/<int:articleid>', views.details, name="details"),
    path('developers/', views.developers, name="developers"),
    path('detect/', views.detect_fake_news, name='detect')
]
