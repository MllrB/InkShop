from django import forms
from .models import UserProfile, DeliveryAddress


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'full_name', 'profile_pic_url',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set focus on full name field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'billing_address_line1': 'Address Line 1',
            'billing_address_line2': 'Address Line 2',
            'billing_town_or_city': 'Town/City',
            'billing_county': 'County',
            'billing_post_code': 'Postcode/Eircode',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'billing_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False


class UserDeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set focus on address reference field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'address_ref': 'Delivery Address Reference',
            'contact_name': 'Delivery Contact Name',
            'contact_phone_number': 'Delivery Contact Phone Number',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'town_or_city': 'Town/City',
            'county': 'County',
            'post_code': 'Postcode/Eircode',
        }

        self.fields['address_ref'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
