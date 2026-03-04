from django.urls import path
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from store.views import *

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list),
    path('products/<int:id>/', product_detail),
    
    # collections
    path('collections/', collection_list),
    path('collections/<int:id>', collection_detail)
]

