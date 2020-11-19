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
    path('readAloud/<int:newsid>/<int:articleid>', views.readAloud, name='readAloud'),
    path('stop/', views.stop, name='stop'),
    path('details/<int:newsid>/<int:articleid>', views.details, name="details"),
    path('developers/', views.developers, name="developers"),
    path('detect/', views.detect_fake_news, name='detect'),
    path('login/', views.loginFunction, name='login'),
    path('foryou/<int:user_id>/', views.for_you, name='for_you'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutFunction, name='logout'),
    path('profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('username/<int:user_id>', views.changeUsername, name='change_username'),
    path('password/<int:user_id>', views.changePassword, name='change_password'),
    path('categories/<int:user_id>', views.changeCategories, name='change_categories'),
    path('newspapers/<int:user_id>', views.changeNewspapers, name='change_newspapers'),
    path('voice/', views.voice_command1, name='voice_command1'),
    path('about/', views.about, name='about')

]
