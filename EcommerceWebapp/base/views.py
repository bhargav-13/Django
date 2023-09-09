from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UserAdminCreationForm,BrandForm, ProductForm, Orderform
from django.contrib.auth.decorators import login_required
from .models import Brand, Product, Category, Cart, OrderItem
from django.conf import settings
from django.http import JsonResponse
import requests
import json

def home(request):
    products = Product.objects.filter(id__lte = 6)

    return render(request, 'base/index.html',{
        'products': products,
    })

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid phone number or password')
    else:
        form = AuthenticationForm()

    context = {'forms' : form, 'page': page}
    return render(request, 'base/login.html', context)


def registerpage(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, "An Error During Registration")
        
    return render(req, 'base/login.html', {'form': form})
    

def about(request):
    return render(request, "base/about.html")

def logoutpage(request):
    logout(request)

    return redirect('home')

@login_required(login_url='/login')
def add_brand(request):
    form = BrandForm(request.POST or None,  request.FILES, owner=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BrandForm()

    context = {"forms": form}
    return render(request, 'base/add-brand.html', context)

@login_required(login_url='/login')
def add_product(request):
    current_user = request.user
    brandName = Brand.objects.filter(owner = current_user)
    print(brandName)
    form = ProductForm(request.POST or None, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
        form.fields['brand'].queryset = brandName

    context = {'forms': form}
    return render(request, 'base/add-product.html', context)

def showProduct(request):
    products = Product.objects.all()
    current_user = request.user
    brandName = Brand.objects.filter(owner = current_user).values_list('name', flat=True)
    byUserBrand = Product.objects.filter(brand__name__in = brandName.all())
    
    context = {'products': products, 'byUserBrand': byUserBrand}
    return render(request, 'base/view-product.html', context)

def contact(request):
    return render(request, 'base/contact.html')

def ProductsByCategories(request, category_id):
    allCategory = Category.objects.all()

    if(category_id == 0):
        products = Product.objects.all()
    else:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    
    context = {'products': products, 'allCategory': allCategory}
    return render(request, 'base/product.html', context)

def ProductDetails(request, pid):
    productDet = Product.objects.get(id=pid)

    context = {'p': productDet}

    return render(request, 'base/product-details.html', context)

def CartView(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = user_cart.products.all()
    
    total = user_cart.calculate_total()
    
    num_items = len(cart_products)
    
    return render(request, 'base/cart.html', {
        'products': cart_products, 
        'subtotal': total,
        'total': total+50,
        'item_num': num_items
    })

def AddToCart(request, pk):
    product = Product.objects.get(pk = pk)
    print(product)
    user = request.user
    
    cart, created = Cart.objects.get_or_create(user=user)
    
    # Add the product to the cart
    cart.products.add(product)
    
    return redirect('cart')

# def create_order(request):
#     form = Orderform()
    
#     if request.method == 'POST':
#         cart = Cart.objects.get(user = request.user)
#         total = cart.calculate_total()
#         form = Orderform(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.total = total
#             order.user = request.user
#             order.save()
            
#             for cart_item in cart.products.all():
#                 order_item = OrderItem(
#                     order=order,
#                     product=cart_item,
#                     quantity=1
#                 )
#                 order_item.save()
            
#             return redirect('success_oc')
#         else:
#             form = Orderform()
            
#     return render(request, 'base/create_order.html', {
#         'form': form,
#     })
    

def create_order(request):
    form = Orderform()
    
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        total = cart.calculate_total()
        form = Orderform(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)
            order.total = total
            order.user = request.user
            order.save()
            
            for cart_item in cart.products.all():
                order_item = OrderItem(
                    order=order,
                    product=cart_item,
                    quantity=1
                )
                order_item.save()
            
            # Prepare the order data to send to the API
            
            if order.is_prepaid == True:
                pay_mode = "prepaid"
            else:
                pay_mode = "COD"
            
            order_data = {
                "data":{
                    "shipments": [
                        {
                            "waybill": "",
                            "order": str(order.order_no),  # Use the order's ID as the order reference
                            "sub_order": "A",
                            "order_date": "31-01-2018",
                            "total_amount": str(total),  # Convert total to string
                            "name": order.user.email,
                            "add": order.user.address,
                            "add2": "",
                            "add3": "",
                            "pin": "362001",
                            "city": order.state,
                            "state": order.state,
                            "country": order.coutry,
                            "phone": order.user.phone_no,
                            "alt_phone": order.user.phone_no,
                            "email": order.user.email,
                            "is_billing_same_as_shipping": "yes",
                            "products": [
                                {
                                    "product_name": item.name,
                                    "product_sku": "GC001-1",
                                    "product_quantity": "1",  # Convert quantity to string
                                    "product_price": str(item.price),  # Convert price to string
                                    "product_tax_rate": "18",  # Convert tax rate to string
                                    "product_hsn_code": "91308",
                                    "product_discount": "0",  # Convert discount to string
                                }
                                for item in cart.products.all()
                            ],
                            "shipment_length": "12",
                            "shipment_width": "16",
                            "shipment_height": "1",
                            "weight": "2.26",
                            "shipping_charges": "0",
                            "giftwrap_charges": "0",
                            "transaction_charges": "0",
                            "total_discount": "0",
                            "first_attemp_discount": "0",
                            "cod_charges": "0",
                            "advance_amount": "0",
                            "cod_amount": "300",
                            "payment_mode": pay_mode,
                            "reseller_name": "",
                            "eway_bill_number": "",
                            "gst_number": "",
                            "return_address_id": "1293"
                        }
                    ],
                    "pickup_address_id": "1293",
                    "access_token": settings.ITL_ACCESS_TOKEN,
                    "secret_key": settings.ITL_SECRET_KEY,
                    "logistics": "",
                    "s_type": "",
                    "order_type": ""
                }
            }

            # print(order_data)
            
            # order_data = json.dumps(order_data)
            
            # print("After Conversion:", order_data)
            # Send the order data to the API
            api_response = send_order_to_api(order_data)
            
            print(api_response)
                  
            return redirect('view-product')
        else:
            form = Orderform()

    return render(request, 'base/create_order.html', {
        'form': form,
    })
    
    
def send_order_to_api(order_data):
    # Define the API endpoint URL where you want to send the order data
    api_url = 'https://pre-alpha.ithinklogistics.com/api_v3/order/add.json'  # Replace with your API URL
    
    headers = {
        "Content-Type": "application/json",
        'cache-control': "no-cache"
    }
    
    try:
        # Make a POST request to the API with the order data
        response = requests.post(api_url, json=order_data, headers=headers)
        
        print(response.text)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and return the API response as a dictionary
            return response.json()
        else:
            # Handle the case where the API request was not successful
            return {"error": "API request failed with status code: {}".format(response.status_code)}
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the API request
        return {"error": "API request failed: {}".format(str(e))}
 
    