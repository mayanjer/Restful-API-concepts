from django.urls import path
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from store.views import *
from rest_framework.routers import SimpleRouter

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'


router = SimpleRouter()
router.register("products", ProductViewSet)
router.register('collections', CollectionViewSet)



urlpatterns = [
    path('', include(router.urls))
    # path('admin/', admin.site.urls),
    # path('products/', ProductList.as_view()),
    # path('products/<int:pk>/', ProductDetail.as_view()),
    
    # # collections
    # path('collections/', collection_list),
    # path('collections/<int:pk>', CollectionDetail.as_view())
]

