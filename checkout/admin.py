from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('total_price',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_number', 'date',  'user_profile', 'order_subtotal', 'order_VAT',
                       'delivery_cost', 'grand_total', 'payment_processor', 'payment_id')

    fields = ('order_number', 'date', 'user_profile', 'customer_name', 'email',
              'phone_number', 'order_address_line1', 'order_town_or_city',
              'order_county', 'order_country', 'order_post_code',
              'order_subtotal', 'order_VAT', 'delivery_cost', 'grand_total',
              'payment_processor', 'payment_id')

    list_display = ('order_number', 'date', 'user_profile', 'customer_name',
                    'order_subtotal', 'order_VAT', 'delivery_cost', 'grand_total',
                    'payment_processor', 'payment_id')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
