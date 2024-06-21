from django.urls import path

from stocks import views

urlpatterns = [
    path("category/create", views.createNewCategory),
    path("category/get-list", views.getAllCategories),
    path("create", views.createStock),
    path("order/placed", views.placeOrder),
]