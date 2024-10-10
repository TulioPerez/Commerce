from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("bids/", views.bids, name="bids"),

    path("selling/", views.selling, name="selling"),
    path("purchases/", views.purchases, name="purchases"),
    path("sell/", views.sell, name="sell"),

    path("item/<int:listing_id>", views.listing_detail, name="listing_detail"),

    # category view for index page
    path("categories/<int:category_id>", views.categories, name="categories"),
    # category view for category list
    path("categories/", views.categories, name="categories"),
    # sell

    path("category/<int:category_id>", views.category_detail, name="category_detail"),
]


# for image rendering
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
