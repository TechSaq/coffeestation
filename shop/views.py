from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Category, Item, OrderItem, Order, Payment
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
        if category == 'coffee-tools':
            c = 'CT'
        if category == 'coffee-cups':
            c = 'CC'
        if category == 'imported-coffee':
            c = 'IC'

        context = {
            'categories': Category.objects.all(),
            'items': Item.objects.filter(category=c),
            'category_param': category,
            'shop':True
        }
        return render(self.request, 'shop.html', context)
    
    

class ProductSingleView(ListView):

    def get(self, *args, **kwargs):

        slug = self.kwargs['slug']
        context = {
            'slug': slug,
            'item': Item.objects.get(slug=slug),
        }
        return render(self.request, 'product-single.html', context)


class CartView(LoginRequiredMixin, View):
    
   print("inside view")

   def get(self, *args, **kwargs):
       cart_items = Order.objects.filter(user=self.request.user, is_ordered=False)
       print("inside func")
       if cart_items.exists():
            context = {
                'cart_items': cart_items[0],
                'cart': True
            }
            print("inside if")
            return render(self.request, 'cart.html', context)
       else:
            messages.info(self.request, "No products available. Redirecting to homepage")
            print("inside else")
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

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        
        order_qs = Order.objects.filter(user=self.request.user, is_ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            form = CheckoutForm()
            
            context = {
                'order': order,
                'form': form,
                'checkout':True
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


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        print("----------------") 
        print(order)

        if order:
            if order.billing_address:
                stripe.api_key = 'sk_test_3pALFqN1hDtd3CojPFW88dWi009Ybdrqsy'
                amount = int(order.get_cart_total())

                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency='usd',
                    # Verify your integration in this guide by including this parameter
                    metadata={'integration_check': 'accept_a_payment'},
                )
                context ={
                    'cart_items': order,
                    'client_secret': intent.client_secret
                }
                return render(self.request, 'payment.html', context)
            else:
                messages.info(self.request, "Add billing address first!")
                return redirect("shop:checkout")
        else:
            messages.info(self.request, "You don't have any order to pay !!")
            return redirect("shop:shop")


    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        amount = int(order.get_cart_total())

        try:
            stripe.api_key = 'sk_test_3pALFqN1hDtd3CojPFW88dWi009Ybdrqsy'

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                # Verify your integration in this guide by including this parameter
                metadata={'integration_check': 'accept_a_payment'},
            )

            payment = Payment(stripe_charge_id=intent['id'],
                                user=self.request.user,
                                amount=amount,
                            )
            payment.save()

            order_item = order.items.all()
            order_item.update(is_ordered=True)
            for item in order_item:
                item.save()

            order.is_ordered = True
            order.payment = payment
            order.save()
            
            messages.success(self.request, "Your order has been placed successfully!!")
            messages.success(self.request, "Thanks for shopping!!")
            return redirect("core:home")
        except stripe.error.CardError as e:
            messages.warning(self.request, f"{ e.error.message }")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, 'Rate Limit Error')
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, 'Invalid parameters')
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, 'Not Authenticated')
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, 'Network error')
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, 'Something went wrong. You were not charged. Try Again!!')
            return redirect("/")
        except Exception as e:
            # send an emaill to ourselves
            print(e)
            messages.warning(
                self.request, 'A serious error occured. We are notified and working on it.')
            return redirect("/")
