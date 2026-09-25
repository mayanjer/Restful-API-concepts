from rest_framework import serializers
from .models import *
from decimal import Decimal
from django.db.models import Sum

class CollectionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "price_with_tax", "collection"]
    price = serializers.DecimalField(max_digits=4, decimal_places=2, source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    collection = CollectionMiniSerializer()
   
    
    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    
    def update(self, instance, validated_data):
        collection_title = validated_data.pop("collection")
        title = collection_title.get("title")
        collection = Collection.objects.get(title = title)
        instance.collection = collection
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
           
        instance.save()
        return instance
    
class CollectionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Collection
        fields = ["id", "title", "product_count"]   
        
    product_count = serializers.SerializerMethodField(method_name="calculate_product_count")
    
    def calculate_product_count(self, collection):
        return collection.products.count()
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "date"]
        
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id = product_id, **validated_data)
    
class MiniProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]
    
    
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "total_price"]
   
    product = MiniProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="calculate_total_price")
    
    def calculate_total_price(self, cart_item):
        product_total = cart_item.product.unit_price * cart_item.quantity
        return product_total
    
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many = True, read_only = True)
    total_price = serializers.SerializerMethodField(method_name="calculate_total_cart_price")
    
    def calculate_total_cart_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Customer
        fields = ["id", "user_id", "birth_date", "phone", "membership"]

        
class OrderItemSerializer(serializers.ModelSerializer):
    product = MiniProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id", "product", "unit_price", "quantity"]
        
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "customer", "placed_at", "payment_status", "items"]