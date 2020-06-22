from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Category, Item, OrderItem, Order
from core.models import Address

from .forms import CheckoutForm

import stripe

def is_valid_form(values):
    valid = True
    for value in values:
        if value == '':
            valid = False
            return valid
    return valid

class ShopView(ListView):
    
    def get(self, *args, **kwargs):
        
        category = self.kwargs['category']
        c=''
        if category == 'coffee-machines':
            c = 'CM'
        if category == 'coffee-making-tools':
            c = 'CT'
        if category == 'coffee-cups':
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

       if cart_items.exists():
            context = {
                'cart_items': cart_items[0]
            }
            return render(self.request, 'cart.html', context)
       else:
            messages.info(self.request, "No products available. Redirecting to homepage")
            # add template 404 
            return redirect("core:home")

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
        
        order_qs = Order.objects.filter(user=self.request.user, is_ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            form = CheckoutForm()
            
            context = {
                'order': order,
                'form': form
            }
            return render(self.request, "checkout.html", context)
        else:
            messages.info(self.request, "No products available. Redirecting to homepage.")
            # add template 404
            return redirect("core:home")
    
    def post(self, *args, **kwargs):

        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.filter(user=self.request.user, is_ordered=False)[0]

            if form.is_valid():
                print("inside valid form")
                use_default = form.cleaned_data.get('use_default')
                
                if use_default:
                    address_qs = Address.objects.filter(user=self.request.user,
                                                        default=True,
                                                        address_type='B')
                    if address_qs.exists():
                        print("using default address")
                        address = address_qs[0]
                        order.billing_address = address
                        order.save()
                    else:
                        print('no default address')
                        messages.info(self.request, "No default address available!")
                        return redirect("shop:checkout")
                else:
                    print('user is entering the address')
                    street_address = form.cleaned_data.get('street_name')
                    apartment_address = form.cleaned_data.get('apartment')
                    country = form.cleaned_data.get('country')
                    zipcode = form.cleaned_data.get('zipcode')

                    if is_valid_form([street_address, country, zipcode]):
                        print("everything is fine")
                        address = Address(
                            user=self.request.user,
                            street_address=street_address,
                            apartment_address=apartment_address,
                            country=country,
                            zipcode=zipcode,
                            address_type='B'
                        )

                        address.save()
                        order.billing_address = address
                        order.save()

                        set_default = form.cleaned_data.get('set_default')
                        if set_default:
                            address.default = True
                            address.save()
                    else:
                        print("empty fields values")
                        messages.warning(self.request, "Please enter the values in the form field!")
                        return redirect("shop:checkout")

            else:
                print("not a valid form")
                messages.info("Please enter valid details!!")
        except:
            pass

        return redirect("shop:payment")


class PaymentView(View):
    def get(self, *args, **kwargs):
        
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        if order.billing_address:
            context ={
                'cart_items': order
            }
            return render(self.request, 'payment.html', context)
        else:
            messages.info(self.request, "Add billing address first!")
            return redirect("shop:checkout")
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_cart_total())

        charge = stripe.PaymentIntent.create(
            amount=1099,
            currency='inr', 
        )

        return redirect("core:home")
