from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from store.serializers import *
from store.models import Product, Collection

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    
    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk = self.kwargs["pk"])
        if product.orderitem_set.count() > 0:
            return Response({"error": "Product has a corresponding order item(s)"}, status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
# class ProductList(ListCreateAPIView): # class based view
#     # def get(self, request):
#     #     query_set = Product.objects.select_related('collection')
#     #     serializer = ProductSerializer(query_set, many = True) 
#     #     return Response(serializer.data)
    
#     # def post(self, request): # this endpoint fails
#     #     serializer = ProductSerializer(data = request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     return Response(serializer.data)
    
#     queryset = Product.objects.select_related('collection')
#     serializer_class = ProductSerializer
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
        
       
# @api_view(["GET", "POST"])
# def collection_list(request): #function based view
#     if request.method == "GET":
#         queryset = Collection.objects.all()
#         serializer = CollectionSerializer(queryset, many = True)
        
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = CollectionSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

    # function based view
# @api_view(["GET", "PUT", "DELETE"])
# def collection_detail(request, id):
#     collection = get_object_or_404(Collection, pk = id)
    
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         if collection.products.count()>0:
#             return Response({"error": "collection has products related to it"}, status.HTTP_403_FORBIDDEN)
#         collection.delete()
#         return Response(status.HTTP_202_ACCEPTED)  
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
    # this is a generic view
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
 
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk = self.kwargs["pk"])
        if collection.products.count() > 0:
            return Response({"error": "Collection has corresponding products in it"}, status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs["product_pk"])
    
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}