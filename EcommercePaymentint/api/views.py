from django.shortcuts import render
from django.http import JsonResponse
from .api_integration import create_order
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_order_view(request):
    if request.method == "POST":
        # Define your order data here
        order_data = {
    "data": {
        "shipments": [
            {
                "waybill": "",  # Leave this empty for the API to generate a waybill number
                "order": "GK0033",  # Your order ID
                "sub_order": "A",  # Sub-order ID or reference
                "order_date": "31-01-2018",  # Order date (format may vary)
                "total_amount": "999",  # Total order amount
                "name": "Bharat",  # Customer's name
                "company_name": "ABC Company",  # Customer's company name (optional)
                "add": "104, Shreeji Sharan",  # Customer's address line 1
                "add2": "",  # Customer's address line 2 (optional)
                "add3": "",  # Customer's address line 3 (optional)
                "pin": "400067",  # PIN code
                "city": "Mumbai",  # City
                "state": "Maharashtra",  # State
                "country": "India",  # Country
                "phone": "9876543210",  # Customer's phone number
                "alt_phone": "9876543210",  # Alternate phone number (optional)
                "email": "abc@gmail.com",  # Customer's email address
                "is_billing_same_as_shipping": "no",  # Whether billing address is the same as shipping address
                "billing_name": "Bharat",  # Billing name (if different from shipping)
                "billing_company_name": "ABC Company",  # Billing company name (optional)
                "billing_add": "104, Shreeji Sharan",  # Billing address line 1
                "billing_add2": "",  # Billing address line 2 (optional)
                "billing_add3": "",  # Billing address line 3 (optional)
                "billing_pin": "400067",  # Billing PIN code
                "billing_city": "Mumbai",  # Billing city
                "billing_state": "Maharashtra",  # Billing state
                "billing_country": "India",  # Billing country
                "billing_phone": "9876543210",  # Billing phone number
                "billing_alt_phone": "9876543210",  # Billing alternate phone number (optional)
                "billing_email": "abc@gmail.com",  # Billing email address
                "products": [
                    {
                        "product_name": "Green color tshirt",  # Product name
                        "product_sku": "GC001-1",  # Product SKU
                        "product_quantity": "1",  # Quantity of this product in the order
                        "product_price": "100",  # Price of the product
                        "product_tax_rate": "5",  # Tax rate for the product
                        "product_hsn_code": "91308",  # HSN code for the product
                        "product_discount": "0"  # Discount for the product
                    },
                    {
                        "product_name": "Red color tshirt",  # Another product
                        "product_sku": "GC002-2",
                        "product_quantity": "1",
                        "product_price": "200",
                        "product_tax_rate": "5",
                        "product_hsn_code": "91308",
                        "product_discount": "0"
                    }
                ],
                "shipment_length": "10",  # Length of the shipment
                "shipment_width": "10",  # Width of the shipment
                "shipment_height": "5",  # Height of the shipment
                "weight": "400",  # Weight of the shipment
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
                "return_address_id": "24"  # Return address ID
            }
                ],
                "pickup_address_id": "24",  # Pickup address ID
                "access_token":  settings.ITL_ACCESS_TOKEN,  # Your access token
                "secret_key": settings.ITL_SECRET_KEY,  # Your secret key
                "logistics": "Delhivery",  # Logistics provider
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

