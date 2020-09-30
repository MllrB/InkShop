import json
import time

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderItem
from customers.models import UserProfile, DeliveryAddress
from products.models import Product


class StripeWH_Handler:
    """
    Handling webhooks from Stripe
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """ Send the user a confirmation email """
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})

        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

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

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        grand_total = round(intent.charges.data[0].amount/100, 2)

        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1

        while attempt <= 8:
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
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook Recieved: {event["type"]}: Order verified in database',
                status=200
            )
        else:
            order = None
            try:
                user_email = billing_details.email
                username = intent.metadata.username
                if username != 'AnonymousUser':
                    user_profile = UserProfile.objects.get(email=user_email)
                    delivery_address_ref = intent.metadata.address_ref
                    if delivery_address_ref:
                        user_delivery_addresses = user_profile.delivery_address.all()
                        match_not_found = True
                        for address in user_delivery_addresses:
                            if address.address_ref == delivery_address_ref:
                                match_not_found = False

                        if match_not_found:
                            DeliveryAddress.objects.create(
                                user=user_profile,
                                address_ref=delivery_address_ref,
                                contact_name=shipping_details.name,
                                contact_phone_number=shipping_details.phone,
                                address_line1=shipping_details.address.line1,
                                address_line2=shipping_details.address.line2,
                                town_or_city=shipping_details.address.city,
                                county=shipping_details.address.state,
                                post_code=shipping_details.address.postal_code,
                                country=shipping_details.address.country
                            )
                else:
                    user_profile = None

                order = Order.objects.create(
                    user_profile=user_profile,
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
                    product = get_object_or_404(Product, pk=item_id)
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
        self._send_confirmation_email(order)
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
