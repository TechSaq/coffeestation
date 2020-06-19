from django.db import models
from django.shortcuts import reverse
from django.conf import settings

from core.models import Address

CATEGORY_CHOICES = [
    ('NO', 'Select Category'),
    ('CM','Coffee Machines'),
    ('CT','Coffee Making Tools'),
    ('CC', 'Coffee Cups'),
]
class Category(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50, 
                                choices=CATEGORY_CHOICES, 
                                default='SELECT CATEGORY')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
            return self.title

    def get_absolute_url(self):
        # return reverse("shop:products", kwargs={"slug": self.slug})
        return reverse("shop:products", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = 'Categories'


class Item(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product_single",
                       kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart",
                       kwargs={"slug": self.slug})

    def get_remove_one_from_cart_url(self):
        return reverse("shop:remove-one-from-cart",
                       kwargs={"slug": self.slug})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title + "  " + self.user.username
    
    def get_total_item_price(self):
        return self.item.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    is_ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(Address,
                                        related_name="billing_address",
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    shipping_address = models.ForeignKey(Address,
                                        related_name="shipping_address",
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
                                        

    def __str__(self):
        return self.user.username

    def get_cart_total(self):
        total = 0.0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()

        return total