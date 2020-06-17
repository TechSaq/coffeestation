from django.urls import path

from shop.views import (ShopView,
                        ProductSingleView, 
                        CartView, 
                        CheckoutView,
                        add_to_cart)
app_name = 'shop'

urlpatterns = [
    path('<str:category>', ShopView.as_view(), name='shop'),
    path('product-single/<slug>', ProductSingleView.as_view(), name='product_single'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
