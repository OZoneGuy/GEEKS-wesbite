from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:event_id>/', views.details, name='details'),
    path('new/', views.new, name='new'),
    path('edit/<int:event_id>/', views.edit, name='edit'),
]
