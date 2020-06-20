from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (
        ('S','Stripe'),
        ('P','Paypal'),
    )

    first_name = forms.CharField(max_length=20,
                                 widget=forms.TextInput(
                                     attrs={'class':'form-control'}
                                 ))
    last_name = forms.CharField(max_length=20,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}
                                ))
    phone = forms.CharField(max_length=15,
                            widget=forms.TextInput(
                                attrs={'class':'form-control'}
                            ))
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(
                                attrs={'class': 'form-control'}
                             ))
    street_name = forms.CharField(max_length=30,
                                  widget=forms.TextInput(
                                    attrs={'class': 'form-control'}
                                  ))
    apartment = forms.CharField(max_length=30,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}
                            ))
    city = forms.CharField(max_length=20,

                           widget=forms.TextInput(
                               attrs={'class': 'form-control'}
                           ))
    zipcode = forms.CharField(max_length=6,
                            widget=forms.TextInput(
                                attrs={'class':'form-control'}
                            ))
    country = CountryField(blank_label='--SELECT COUNTRY--').formfield(
        widget=CountrySelectWidget(
            attrs={'class':'form-control'}
        )
    )

    payment_choice = forms.ChoiceField(choices=PAYMENT_CHOICES,
                                       widget=forms.RadioSelect(
                                        attrs={'class':'mr-2'}
                                       )
                                    )
