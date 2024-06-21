
from django.urls import path

from vendordetails import views

urlpatterns = [
    path("register", views.registerVendor),
    path("login", views.loginVendor),
    path("create-inventory", views.createInventory),
    path('get-order-details', views.getOrderDetails)
]
