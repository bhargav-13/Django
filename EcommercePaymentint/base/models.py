from django.db import models
from django.contrib.auth.models import User
import uuid


class Warehouse(models.Model):
    company_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    city_id = models.CharField(max_length=10)
    state_id = models.CharField(max_length=10)
    country_id = models.CharField(max_length=10)

    def __str__(self):
        return self.company_name

class Store(models.Model):
    store_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    store_email = models.EmailField()
    store_website_name = models.CharField(max_length=255)
    store_url = models.URLField()
    platform_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Add a foreign key relationship with Warehouse model
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, related_name='stores')

    def __str__(self):
        return self.store_name

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=50)
    product_quantity = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    product_hsn_code = models.CharField(max_length=10)
    product_discount = models.DecimalField(max_digits=10, decimal_places=2)
    shipment_length = models.DecimalField(max_digits=5, decimal_places=2)
    shipment_width = models.DecimalField(max_digits=5, decimal_places=2)
    shipment_height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Address"
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to="base/static/base/images/products/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    @property
    def total_cost(self):
        return self.quantity * self.product.product_price


class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, related_name='orders')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='shipping_orders', null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='billing_orders', null=True)
    billing_same_as_shipping = models.BooleanField(default=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)
    gst_number = models.CharField(max_length=15, blank=True, null=True)  # GST number for the order

    def calculate_shipment_dimensions(self):
        shipment_length = sum(item.product.shipment_length for item in self.orderitem_set.all())
        shipment_width = sum(item.product.shipment_width for item in self.orderitem_set.all())
        shipment_height = sum(item.product.shipment_height for item in self.orderitem_set.all())
        weight = sum(item.product.weight for item in self.orderitem_set.all())
        return shipment_length, shipment_width, shipment_height, weight

    def __str__(self):
        return f"Order #{self.order_number}"

    class Meta:
        ordering = ['-order_date']  # Sort orders by order_date in descending order
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item in Order #{self.order.id}: {self.product.product_name}"

