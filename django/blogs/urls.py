from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:blog-id>', views.details, name='details')
]
