from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView

from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Item, OrderItem, Order


class ShopView(ListView):
    
    def get(self, *args, **kwargs):
        
        category = self.kwargs['category']
        c=''
        if category == 'category-cm':
            c = 'CM'
        if category == 'category-cmt':
            c = 'CT'
        if category == 'category-cc':
            c = 'CC'

        context = {}
        context['categories'] = Category.objects.all()
        context['items'] = Item.objects.filter(category=c)
        context['category_param'] = category
        return render(self.request, 'shop.html', context)
    
    

class ProductSingleView(ListView):

    def get(self, *args, **kwargs):

        slug = self.kwargs['slug']
        context = {
            'slug': slug
        }
        return render(self.request, 'product-single.html', context)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        is_ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    print(order_qs)
    if order_qs.exists():
        print(order_qs)
        return redirect("shop:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        order.items.add(order_item)
        return redirect("shop:cart")


    return redirect("shop:cart")
    

class CheckoutView(TemplateView):
    template_name = "checkout.html"

