from django.shortcuts import render
from .models import Product, CartItem
from django.http import HttpResponse


def product_list(request):
    # products = Product.objects.all()
    # return render(request, 'store/product_list.html', {'products': products})
    return HttpResponse("<h1>All Products...</h1>")

def product_detail(request, product_id):
    # product = Product.objects.get(id=product_id)
    # return render(request, 'store/product_detail.html', {'product': product})
    pass

def cart(request):
    cart_items = CartItem.objects.filter(user=1)
    
    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    return render(request, 'base/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
        })