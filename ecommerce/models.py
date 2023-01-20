from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    # slug = models.SlugField()

    @property
    def price_sale(self):
        return float(self.price) * 0.8

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_card')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='user_product')
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=0, default=0)

    def __str__(self):
        return f'{self.user} -> {self.product} -> {self.quantity} -> ${self.total_price} in total'

