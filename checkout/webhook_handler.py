import json
import time

from django.http import HttpResponse

from .models import Order, OrderItem
from products.models import Product


class StripeWH_Handler:
    """
    Handling webhooks from Stripe
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unkwown/unexpected webhook from stripe
        """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle a payment_intent.succeeded webhook from stripe
        """

        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        delivery_address_ref = intent.metadata.address_ref

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        grand_total = round(intent.charges.daat[0].amount/100, 2)

        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1

        while attempt <= 10:
            try:
                order = Order.objects.get(
                    customer_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    order_address_line1__iexact=shipping_details.address.line1,
                    order_address_line2__iexact=shipping_details.address.line2,
                    order_town_or_city__iexact=shipping_details.address.city,
                    order_county__iexact=shipping_details.address.state,
                    order_country__iexact=shipping_details.address.country,
                    order_post_code__iexact=shipping_details.address.postal_code,
                    grand_total=grand_total,
                    original_basket=basket,
                    payment_id=pid,
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook Recieved: {event["type"]}: Order verified in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    customer_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    order_address_line1=shipping_details.address.line1,
                    order_address_line2=shipping_details.address.line2,
                    order_town_or_city=shipping_details.address.city,
                    order_county=shipping_details.address.state,
                    order_country=shipping_details.address.country,
                    order_post_code=shipping_details.address.postal_code,
                    original_basket=basket,
                    payment_id=pid,
                )
                for item_id, item_qty in json.loads(basket).items():
                    product = Product.objects.get(pk=item_id)
                    order_line = OrderItem(
                        order=order,
                        product=product,
                        quantity=item_qty,
                    )
                    order_line.save()
            except Exception as error:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]}: ERROR {error}',
                    status=500
                )

        return HttpResponse(
            content=f'Webhook received: {event["type"]}: SUCCESS: Order created in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle a payment_intent.payment_failed webhook from stripe
        """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
