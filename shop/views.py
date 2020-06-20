from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Category, Item, OrderItem, Order
from .forms import CheckoutForm


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

        context = {
            'categories': Category.objects.all(),
            'items': Item.objects.filter(category=c),
            'category_param': category
        }
        return render(self.request, 'shop.html', context)
    
    

class ProductSingleView(ListView):

    def get(self, *args, **kwargs):

        slug = self.kwargs['slug']
        context = {
            'slug': slug
        }
        return render(self.request, 'product-single.html', context)


class CartView(LoginRequiredMixin, ListView):

   def get(self, *args, **kwargs):
       cart_items = Order.objects.filter(user=self.request.user)
       context = {
           'cart_items': cart_items[0]
       }
      
       return render(self.request, 'cart.html', context)

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        is_ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
   
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(user=request.user, is_ordered=False):
            order_item.quantity += 1
            order_item.save()
            order.items.add(order_item)
            messages.info(request, "This item has been updated!")
            return redirect("shop:cart")
        else:
            messages.info(request, "This item has been added to cart!")
            order.items.add(order_item)
            return redirect("shop:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        messages.info(request, "This item has been added to cart!")
        order.items.add(order_item)
        return redirect("shop:cart")
    
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(user=request.user, is_ordered=False):
            order_item = OrderItem.objects.filter(
                item=item,
                is_ordered=False,
                user=request.user
            )[0]

            order_item.quantity = 1
            order_item.save()
            messages.info(request, "This item has been removed from your cart!")
            order.items.remove(order_item)
            return redirect("shop:cart")
        else:
            messages.info(request, "This item is not in your cart!")
            return redirect("shop:cart")
    else:
        message(request, "You don't have any order yet!")
        return redirect("shop:shop",  category="category-cmt")



@login_required
def remove_one_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                is_ordered=False,
                user=request.user
            )[0]
            
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "This item has been updated!")
                return redirect("shop:cart")
            else:
                messages.info(request, "This item has been removed from your cart!")
                order_item.quantity -= 1
                order_item.save()
                order.items.remove(order_item)
                return redirect("shop:shop", category="category-cmt")
        else:
            messages.info(request, "This item is not in your cart!")
            return redirect("shop:cart")
    else:
        messages.info(request, "You don't have any order yet!")
        return redirect("shop:shop", category="category-cmt")

class CheckoutView(LoginRequiredMixin, ListView):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, is_ordered=False)[0]

        form = CheckoutForm()

        context = {
            'order': order,
            'form': form
        }
        return render(self.request, "checkout.html", context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.Post or None)

        if form.is_valid():
            #add default address functionality
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            street_name = form.cleaned_data.get('street_name')
            apartment = form.cleaned_data.get('apartment')
            city = form.cleaned_data.get('city')
            zipcode = form.cleaned_data.get('zipcode')
            country = form.cleaned_data.get('country')
            payment_choice = form.cleaned_data.get('payment_choice')

            print("-------------------")
            print(first_name)
            print(last_name)
            print(phone)
            print(email)
            print(street_name)
            print(apartment)
            print(city)
            print(zipcode)
            print(country)
            print(payment_choice)
            print("-------------------")

