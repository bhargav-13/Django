from django.shortcuts import render
from rest_framework import generics
from .serializer import CartSerializer
from base.models import Cart

class CartApiView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

