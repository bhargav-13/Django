import requests

url = "https://pre-alpha.ithinklogistics.com/api_v3/order/add.json"

payload = "{\"data\":{\"shipments\":[{\"waybill\":\"\",\"order\":\"GK0034\",\"sub_order\":\"\",\"order_date\":\"31-01-2018\",\"total_amount\":\"999\",\"name\":\"Bharat\",\"company_name\":\"ABC Company\",\"add\":\"104 Shreeji\",\"add2\":\"\",\"add3\":\"\",\"pin\":\"400067\",\"city\":\"Mumbai\",\"state\":\"Maharashtra\",\"country\":\"India\",\"phone\":\"9876543210\",\"alt_phone\":\"9876542210\",\"email\":\"abc@gmail.com\",\"is_billing_same_as_shipping\":\"no\",\"billing_name\":\"Bharat\",\"billing_company_name\":\"ABC Company\",\"billing_add\":\"104, Shreeji Sharan\",\"billing_add2\":\"\",\"billing_add3\":\"\",\"billing_pin\":\"400067\",\"billing_city\":\"Mumbai\",\"billing_state\":\"Maharashtra\",\"billing_country\":\"India\",\"billing_phone\":\"9876543210\",\"billing_alt_phone\":\"9876543211\",\"billing_email\":\"abc@gmail.com\",\"products\":[{\"product_name\":\"Green color tshirt\",\"product_sku\":\"GC001-1\",\"product_quantity\":\"1\",\"product_price\":\"100\",\"product_tax_rate\":\"5\",\"product_hsn_code\":\"91308\",\"product_discount\":\"0\"},{\"product_name\":\"Red color tshirt\",\"product_sku\":\"GC002-2\",\"product_quantity\":\"1\",\"product_price\":\"200\",\"product_tax_rate\":\"5\",\"product_hsn_code\":\"91308\",\"product_discount\":\"0\"}],\"shipment_length\":\"10\",\"shipment_width\":\"10\",\"shipment_height\":\"5\",\"weight\":\"400.00\",\"shipping_charges\":\"0\",\"giftwrap_charges\":\"0\",\"transaction_charges\":\"0\",\"total_discount\":\"0\",\"first_attemp_discount\":\"0\",\"cod_amount\":\"550\",\"payment_mode\":\"COD\",\"reseller_name\":\"\",\"eway_bill_number\":\"\",\"gst_number\":\"\",\"return_address_id\":\"24\"}],\"pickup_address_id\":\"24\",\"access_token\":\"8ujik47cea32ed386b1f65c85fd9aaaf\",\"secret_key\":\"65tghjmads9dbcd892ad4987jmn602a7\",\"logistics\":\"fedex\",\"s_type\":\"ground\",\"order_type\":\"\"}}"
headers = {
          'content-type': "application/json",
          'cache-control': "no-cache"
      }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)