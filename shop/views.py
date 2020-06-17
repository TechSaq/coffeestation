from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Item


class ShopView(ListView):
    template_name = "shop.html"
    model = Category
    context_object_name = 'categories'


    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()
        category = self.kwargs['category']
        c=''
        if category == 'category-cm':
            c = 'CM'
        if category == 'category-cmt':
            c = 'CT'
        if category == 'category-cc':
            c = 'CC'
        context['items'] = Item.objects.filter(category=c)
        context['category_param'] = category
        return context
    
    


class ProductSingleView(TemplateView):
    template_name = "product-single.html"


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"
    

class CheckoutView(TemplateView):
    template_name = "checkout.html"

