from django.urls import path

from . import views

app_name = 'people'

urlpatterns = [
    path('', views.index, name='account'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('password', views.change_pass, name='password'),
    path('membership', views.memberships, name='membership'),
    path('members', views.members, name='members'),
    path('card', views.card, name='card'),
    path('qrcode', views.QRcode, name='qrcode'),
]
