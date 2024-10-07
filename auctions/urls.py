from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("item/<int:listing_id>", views.item_detail, name="item_detail"),

    # category view for index page
    path("categories/<int:category_id>", views.categories, name="categories"),
    # category view for category list
    path("categories/", views.categories, name="categories"),
    # sell

    path("category/<int:category_id>", views.category_detail, name="category_detail"),
]
