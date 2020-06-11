from django.shortcuts import render

def shop(request):
    return render(request, 'shop.html')


def product_single(request):
    return render(request, 'product-single.html')
    

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

