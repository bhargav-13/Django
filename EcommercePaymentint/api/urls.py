from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order_view, name='create_order'),
    # Add more URL patterns for other API endpoints as needed
]
