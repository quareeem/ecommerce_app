from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from .models import Product, Category, CartItem


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = serializers.SlugRelatedField(read_only=False, slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'price_sale', 'category')


class ProductPriceInCartSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('price')



class CartItemSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.SlugRelatedField(read_only=False, slug_field='name', queryset=Product.objects.all())
    prod_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_quantity(self, instance):
        return instance.quantity

    def get_prod_price(self, instance):
        return instance.product.price

    def get_total_price(self, instance):
        return self.get_quantity(instance=instance) * self.get_prod_price(instance=instance)

    class Meta:
        model = CartItem
        fields = ('user', 'id', 'product', 'quantity', 'prod_price', 'total_price') 
          
