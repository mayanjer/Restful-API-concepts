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
router.register('customers', CustomerViewSet, basename="customers")
router.register('orders', OrderViewSet, basename = "orders")


products_router = routers.NestedDefaultRouter(router, "products", lookup = "product")
products_router.register("reviews", ReviewViewSet, basename="product-review")

carts_router = routers.NestedDefaultRouter(router, "carts", lookup = "cart")
carts_router.register("items", CartItemViewSet, basename="cart-items")


try_route = [path("try_collect", collection_list)]

urlpatterns = [
    path('', include(router.urls + products_router.urls +  carts_router.urls+try_route)),
    path('admin/', admin.site.urls),
        
]

