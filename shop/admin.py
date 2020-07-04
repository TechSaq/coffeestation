from django.contrib import admin
from .models import Category, Item, OrderItem, Order, Payment
from django.utils.safestring import mark_safe

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'is_ordered',
                    'is_delivered',
                    'is_received',
                    'billing_address',
                    'payment',
                    'ordered_date'
                    ]
    list_display_links = ['user',
                          'billing_address',
                          'payment',
                          ]
    list_filter = ['is_ordered',
                    'user'
                    ]

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 
                    'image', 
                    'price', 
                    'category'
                    ]
    list_filter = ['category']
    readonly_fields = ["product_image"]

    # to display image in admin
    def product_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width='300px',
            height='auto',
        )
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
