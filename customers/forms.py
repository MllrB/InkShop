from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import UserProfile, DeliveryAddress


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'profile_pic_url', 'profile_pic',
                   'email', 'favourites',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set focus on full name field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Your Full Name',
            'default_phone_number': 'Phone Number',
            'billing_address_line1': 'Address Line 1',
            'billing_address_line2': 'Address Line 2',
            'billing_town_or_city': 'Town/City',
            'billing_county': 'County',
            'billing_post_code': 'Postcode/Eircode',
        }

        # fields reuired by stripe but not immediately on login
        self.fields['default_phone_number'].required = True
        self.fields['billing_country'].required = True

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
        widgets = {
            'id': forms.HiddenInput(),
        }
        fields = [
            'id',
            'address_ref',
            'contact_name',
            'contact_phone_number',
            'address_line1',
            'address_line2',
            'town_or_city',
            'county',
            'post_code',
            'country',
        ]

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set focus on address reference field
        """
        self.user = kwargs.pop('user', None)
        self.updating = kwargs.pop('updating', None)
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

        self.fields['address_line1'].required = True
        self.fields['country'].required = True

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

    def clean_address_ref(self):
        address_ref = self.cleaned_data.get("address_ref")
        user_profile = self.user
        existing_address_refs = DeliveryAddress.objects.all().filter(
            user=user_profile)

        if not self.updating:
            for existing_ref in existing_address_refs:
                if address_ref == existing_ref.address_ref:
                    raise forms.ValidationError(
                        _("Your address reference must be unique."), code="Non unique address reference")

        return address_ref
