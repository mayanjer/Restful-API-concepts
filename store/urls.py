from django.urls import path
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from store.views import *

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),
    
    # collections
    path('collections/', CollectionDetail.as_view()),
    path('collections/<int:pk>', CollectionDetail.as_view())
]

