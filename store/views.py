from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view, action
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from store.serializers import *
from store.models import Product, Collection, Cart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["collection_id"]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "title"]
    permission_classes = [IsAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk = self.kwargs["pk"])
        if product.orderitem_set.count() > 0:
            return Response({"error": "Product has a corresponding order item(s)"}, status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
   
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

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
    
class CartViewSet(ListModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin, 
                  CreateModelMixin, 
                  GenericViewSet):
    
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer
    
class CartItemViewSet(ModelViewSet): 
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        queryset = CartItem.objects.all()
        if self.kwargs != {}:
            queryset = CartItem.objects.filter(cart_id = self.kwargs.get("cart_pk"))
        return queryset
    
    
    
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
    
        
       
@api_view(["GET", "POST"])
def collection_list(request): #function based view
    print(request.user)
    if request.method == "GET":
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many = True)
        
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
 
 
class CustomerViewSet(ModelViewSet):
     queryset = Customer.objects.all()
     serializer_class = CustomerSerializer
     permission_classes = [IsAuthenticated]
     
     
     @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAdminOrReadOnly])
     def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)