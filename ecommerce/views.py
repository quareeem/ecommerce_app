from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer, CartItemSerializer
from .models import Product, Category, CartItem
from .permissions import IsAuthorOrForbidden
import json



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrForbidden]


    @action(detail=False, methods=['get'], url_path='cart_total')
    def cart_total(self, request, *args, **kwargs):
        cart = self.list(self, request, *args, **kwargs)

        items, total = [], 0
        for item in json.loads(json.dumps(cart.data)):
            items.append({item['product']: item['quantity']})
            total += item['total_price']
        
        response = {
            'items': items,
            'in total': total
            }
        return Response(response)
        

    def list(self, request, *args, **kwargs):
        self.queryset = CartItem.objects.filter(user=self.request.user)
        return super(CartItemViewSet, self).list(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        self.queryset = CartItem.objects.filter(user=self.request.user)
        serializer = self.get_serializer(self.queryset, many=True)
        data_str = json.dumps(serializer.data)
        
        prod_name_rq = request.data['product']
        kwargs = {'pk': ''}

       
        if prod_name_rq in data_str:
            data_lst = json.loads(data_str)
            temp_quantity = None

            for item in data_lst:
                if item['product'] == prod_name_rq:
                    self.kwargs['pk'] = item['id']
                    temp_quantity = item['quantity']
                    break
            

            sum_request_data = request.data
            sum_request_data['quantity'] = request.data['quantity'] + temp_quantity

            instance = self.get_object()
            serializer = self.get_serializer(instance, data=sum_request_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return super().create(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        print(kwargs)
        return super().retrieve(request, *args, **kwargs)
        
    

