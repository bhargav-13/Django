from django.shortcuts import render
from .models import Cart, CartItem, Product, ProductImage
from django import template

register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price


def view_cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = calculate_cart_total(cart_items)
    
    
    return render(request, 'base/view_cart.html', {'cart': cart, 'cart_items': cart_items, 'cart_total': cart_total})

def calculate_cart_total(cart_items):
    total = sum(item.product.product_price * item.quantity for item in cart_items)
    return total
