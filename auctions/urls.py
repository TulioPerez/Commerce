from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item_listing", views.item_listing, name="item_listing"), # for individual item details
    path("listings", views.listings, name="listings"), # for lists of listings / catergories
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
