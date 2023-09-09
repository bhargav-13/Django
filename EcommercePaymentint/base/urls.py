from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_cart, name='view_cart'),
]