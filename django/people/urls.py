from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('', views.index, name='account'),
    path('login', views.index, name='login'),
    path('register', views.index, name='register'),
    path('logout', views.index, name='logout'),
]
