from django.shortcuts import render
from django.http import JsonResponse
from .api_integration import create_order, get_all_orders
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets


@csrf_exempt
def create_order_view(request):
    if request.method == "POST":
        # Define your order data here
        order_data = {
    "data": {
        "shipments": [
            {
                "waybill":"",
                "order": "fafde885-8343-4e38-8e7b-fb3a65667adaa",  # Your order ID
                "sub_order": "A",  # Sub-order ID or reference
                "order_date": "31-01-2018",  # Order date (format may vary)
                "total_amount": "55",  # Total order amount
                "name": "bhargav",  # Customer's name
                "add": "kailas nagar-1",  # Customer's address line 1
                "add2": "",  # Customer's address line 2 (optional)
                "add3": "",  # Customer's address line 3 (optional)
                "pin": "362001",  # PIN code
                "city": "junagadh",  # City
                "state": "gujarat",  # State
                "country": "India",  # Country
                "phone": "9624413978",  # Customer's phone number
                "alt_phone": "9898013978",
                "email": "bhargavthesiya@gmail.com",  # Customer's email address
                "is_billing_same_as_shipping": "yes",  # Whether billing address is the same as shipping address
                "products": [
                    {
                        "product_name": "dell laptop",  # Product name
                        "product_sku": "GC001-1",  # Product SKU
                        "product_quantity": "1",  # Quantity of this product in the order
                        "product_price": "55",  # Price of the product
                        "product_tax_rate": "5",  # Tax rate for the product
                        "product_hsn_code": "91308",  # HSN code for the product
                        "product_discount": "0"  # Discount for the product
                    },
                ],
                "shipment_length": "12",  # Length of the shipment
                "shipment_width": "16",  # Width of the shipment
                "shipment_height": "1",  # Height of the shipment
                "weight": "2.26",  # Weight of the shipment
                "shipping_charges": "0",  # Shipping charges
                "giftwrap_charges": "0",  # Gift wrapping charges
                "transaction_charges": "0",  # Transaction charges
                "total_discount": "0",  # Total discount
                "first_attemp_discount": "0",  # First attempt discount
                "cod_charges": "0",  # COD (Cash on Delivery) charges
                "advance_amount": "0",  # Advance payment amount
                "cod_amount": "300",  # COD amount
                "payment_mode": "COD",  # Payment mode
                "reseller_name": "",  # Reseller name (optional)
                "eway_bill_number": "",  # E-way bill number (optional)
                "gst_number": "",  # GST number (optional)
                "return_address_id": "1293"  # Return address ID
            }
                ],
                "pickup_address_id": "1293",  # Pickup address ID
                "access_token":  settings.ITL_ACCESS_TOKEN,  # Your access token
                "secret_key": settings.ITL_SECRET_KEY,  # Your secret key
                "logistics": "",  # Logistics provider
                "s_type": "",  # Shipment type (optional)
                "order_type": ""  # Order type (optional)
            }
        }

        response = create_order(order_data)

        if "error" in response:
            return JsonResponse(response, status=400)  # Return an error response
        else:
            return JsonResponse(response)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def get_all_orders_view(request):
    # Get all orders using the function
    all_orders = get_all_orders()

    if "error" in all_orders:
        # Handle error case
        error_message = all_orders["error"]
        status_code = all_orders["status_code"]
        return JsonResponse({"error": error_message}, status=status_code)

    # Process and return the list of all orders
    return JsonResponse(all_orders)

    
    