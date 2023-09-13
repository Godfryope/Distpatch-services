from django.db import models
import uuid

class Dispatcher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Add a field for phone number
    # You can include more fields like address, employee ID, etc.

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products', height_field=None, width_field=None, max_length=None)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)  # Add a field for product category
    stock_quantity = models.PositiveIntegerField(default=0)  # Add a field for stock quantity

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    # Add more customer-related fields as needed

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('ORDER PLACED', 'Order Placed'),
        ('PENDING CONFIRMATION', 'Pending Confirmation'),
        ('WAITING TO BE SHIPPED', 'Waiting to Be Shipped'),
        ('SHIPPED', 'Shipped'),
        ('OUT FOR DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dispatcher = models.ForeignKey(Dispatcher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem')  # Create a separate OrderItem model for line items
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)  # Default status

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class OrderTracking(models.Model):
    STATUS_CHOICES = (
        ('ORDER PLACED', 'Order Placed'),
        ('PENDING CONFIRMATION', 'Pending Confirmation'),
        ('WAITING TO BE SHIPPED', 'Waiting to Be Shipped'),
        ('SHIPPED', 'Shipped'),
        ('OUT FOR DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    delivery_date = models.DateField(null=True, blank=True)
    tracking_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Use UUIDField

    def __str__(self):
        return f"Tracking for Order #{self.order.id}"
