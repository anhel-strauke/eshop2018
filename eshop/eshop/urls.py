"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from info_pages.views import page_view
from catalog.views import category_view, product_view, main_view, buy_view, cart_view, checkout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/<str:page_name>/', page_view, name="page_view"),
    path('category/<int:cat_id>/', category_view, name="cat_view"),
    path('item/<int:prod_id>/', product_view, name="prod_view"),
    path('item/<int:prod_id>/buy/', buy_view, name="buy_view"),
    path("cart/", cart_view, name="cart_view"),
    path("cart/checkout/", checkout_view, name="checkout_view"),
    path('', main_view, name="main_view"),
]
