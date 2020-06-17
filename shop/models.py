from django.db import models
from django.shortcuts import reverse

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
        return reverse("shop:product-single",
                       kwargs={"slug": self.slug})

    # def get_add_to_cart_url(self):
    #     return reverse("core:add-to-cart",
    #                    kwargs={"slug": self.slug})

    # def get_remove_from_cart_url(self):
    #     return reverse("core:remove-from-cart",
    #                    kwargs={"slug": self.slug})
