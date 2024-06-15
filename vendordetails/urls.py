
from django.urls import path

from vendordetails import views

urlpatterns = [
    path("register", views.registerNewUser),
    path("login", views.loginUser)
]
