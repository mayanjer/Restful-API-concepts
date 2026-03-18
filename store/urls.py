from django.urls import path
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from store.views import *
from rest_framework_nested import routers
from pprint import pprint

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'


router = routers.DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register('collections', CollectionViewSet, basename = "collections")
router.register('carts', CartViewSet, basename = "carts")
router.register('cart_item', CartItemViewSet, basename= "cart_items")

products_router = routers.NestedDefaultRouter(router, "products", lookup = "product")
products_router.register("reviews", ReviewViewSet, basename="product-review")

urlpatterns = [
    path('', include(router.urls + products_router.urls)),
    path('admin/', admin.site.urls),
        
]

