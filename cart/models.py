from django.db import models
from account.models import Account
from product.models import Product
from decimal import Decimal
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True,null=True,default=1)

    def __str__(self):
        return f"Cart for {self.user.email} | {self.products}"

    def total(self):
        return Decimal(self.quantity) * self.products.price
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)