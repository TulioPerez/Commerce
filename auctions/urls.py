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
    path("category/<int:category_id>", views.category, name="category"),
    # category view for category list
    path("category/", views.category, name="category"),
    # sell
]
