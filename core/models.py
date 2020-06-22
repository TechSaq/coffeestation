from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

ADDRESS_CHOICES = {
    ('B', 'Billing'),
    ('S', 'Shipping')
}
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100, null=True)
    country = CountryField()
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
