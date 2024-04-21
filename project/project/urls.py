from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('/', admin.site.urls),
    path('', include('customer.urls')),  
    path('', include('loan.urls')), 
]
                                                                                                                                                                                                                                                                      