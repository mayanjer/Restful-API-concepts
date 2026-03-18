from rest_framework import serializers
from .models import Product, Collection, Review
from decimal import Decimal

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
        fields = ["id", "product", "name", "description", "date"]