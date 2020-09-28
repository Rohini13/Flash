from django.urls import path,include
from . import views

urlpatterns = [
    path('main/', views.index, name='index'),
    path('world/',views.index1, name='index1'),
    path('local/',views.index2, name='index2'),
    path('science_technology/',views.index3, name='index3'),
    path('business_economy/',views.index4, name='index4'),
    path('health_lifestyle/',views.index5,name='index5'),
    path('sports/',views.index6,name='index6'),
    path('entertainment/',views.index7,name='index7'),
    path('readAloud/', views.readAloud, name='readAloud'),
    path('stop/', views.stop, name='stop'),
    path('signin/', views.signIn),
    path('postsign/', views.postsign),
    path('logout/', views.logout, name="log"),
    path('signup/', views.signUp, name="signup"),
    path('postsignup/', views.postsignup, name="postsignup"),
    path('details/<int:newsid>/<int:articleid>', views.details, name="details")
]
