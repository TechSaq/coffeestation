from django.urls import path

from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('product-single/', views.product_single, name='product_single'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]
