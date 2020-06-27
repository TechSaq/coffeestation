from django.urls import path

from shop.views import (ShopView,
                        ProductSingleView, 
                        CartView, 
                        CheckoutView,
                        PaymentView,
                        add_to_cart,
                        remove_one_from_cart,
                        remove_from_cart)
app_name = 'shop'

urlpatterns = [
    path('<category>/', ShopView.as_view(), name='shop'),
    path('product-single/<slug>/', ProductSingleView.as_view(), name='product_single'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-one-from-cart/<slug>/', remove_one_from_cart, name='remove-one-from-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
]
