from django.contrib import admin
from .models import Address


class Addressdmin(admin.ModelAdmin):
    list_display = ['user',
                    'street_address',
                    'apartment_address',
                    'zipcode',
                    'country',
                    'default'
                    ]
    list_filter =['user',
                  'zipcode',
                ]
    search_fields = ['user',
                     'street_address',
                     'apartment_address',
                     'zipcode',
                     'country'
                     ]

admin.site.register(Address, Addressdmin)
