from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("item/<int:listing_id>", views.item_listing, name="item_listing"),
    path("item/<int:category>", views.category, name="category"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register")
    # path("item_listing/", views.item_listing, name="item_listing"), # for individual item details
    # path("listings/", views.listings, name="listings"), # for lists of listings / catergories
    # categories
    # sell
]
