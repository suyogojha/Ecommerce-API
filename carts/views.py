from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated

from carts.models import Cart, CartItems
from products.models import Product
from .models import * 
from .serializer import *
# Create your views here.



class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        user = request.user
        cart = Cart.objects.filter(user = user , ordered = False).first()
        queryset = CartItems.objects.filter(cart = cart)
        serializer = CartItemsSerializer(queryset , many = True)
        return Response(serializer.data)
    
    def post(self , request):
        data = request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user = user, ordered = False)
        
        product = Product.objects.get(id = data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItems.objects.create(cart = cart, product = product, price = price, quantity = quantity)
        cart_items.save()
        
        total_price = 0
        cart_items = CartItems.objects.filter(user = user ,cart = cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        
        return Response({'success' : 'Cart item added successfully'})
    
    def update(self , request):
        data = request.data
        cart_item = CartItems.objects.get(id = data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success' : 'Cart item updated successfully'})
    
    def delete(self , request):
        user = request.user
        data = request.data
        
        cart_item = CartItems.objects.get(id = data.get('id'))
        cart_item.delete()
        
        cart = Cart.objects.filter(user = user , ordered = False).first()
        quetyset = CartItems.objects.filter(cart = cart)
        serializer = CartItemsSerializer(quetyset , many = True)
        return Response(serializer.data)
    
class OrderAPI(APIView):
    def get(self, request):
        queryset = Orders.objects.filter(user = request.user)
        serializer = OrderSerializer(queryset, many = True)
        return Response(serializer.data)