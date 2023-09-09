from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order_view, name='create_order'),
    path('get_all_orders/', views.get_all_orders_view, name='get_all_orders'),
    # Add more URL patterns for other API endpoints as needed
]
