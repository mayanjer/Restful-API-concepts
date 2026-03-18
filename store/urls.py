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
router.register("products", ProductViewSet)
router.register('collections', CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, "products", lookup = "product")
products_router.register("reviews", ReviewViewSet, basename="product-review")

pprint(products_router.urls)




urlpatterns = [
    path('', include(router.urls + products_router.urls))
    # path('admin/', admin.site.urls),
    # path('products/', ProductList.as_view()),
    # path('products/<int:pk>/', ProductDetail.as_view()),
    
    # # collections
    # path('collections/', collection_list),
    # path('collections/<int:pk>', CollectionDetail.as_view())
]

