from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:blog_id>', views.details, name='details'),
    path('new/', views.new, name='new'),
    path('edit/<int:blog_id>', views.edit, name='edit'),
]
