from django.db import models
from account.models import Account,Address
from product.models import Product
from decimal import Decimal
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class Order(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    status = models.CharField(max_length=60,choices=STATUS_CHOICES)
    paid = models.BooleanField(default=False)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,default=None,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    indexes = [
        models.Index(fields=['-created_at']),
    ]

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
    def total(self):
        return Decimal(self.quantity) * self.product.price
    def __str__(self):
        return f"Order {self.order.id}"