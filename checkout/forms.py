from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name', 'email', 'phone_number',
                  'order_address_line1', 'order_address_line2',
                  'order_town_or_city', 'order_county',
                  'order_country', 'order_post_code')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, remove auto generated labels 
        and set autofocus on the first field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'customer_name': 'Your Full Name',
            'email': 'Your Email Address',
            'phone_number': 'Your Phone Number',
            'order_address_line1': 'Street Address Line 1',
            'order_address_line2': 'Street Address Line 2',
            'order_town_or_city': 'Town/City',
            'order_county': 'County',
            'order_country': 'Country',
            'order_post_code': 'Eircode/Postcode',
        }

        self.fields['order_country'].required = True
        self.fields['customer_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
