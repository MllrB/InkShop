from django.http import HttpResponse


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
        print(intent)
        pid = intent.id
        basket = intent.metadata.basket
        delivery_address_ref = intent.metadata.address_ref

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        grand_total = round(intent.charges.daat[0].amount/100, 2)

        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
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
