from django import forms

from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {'price': forms.HiddenInput(),
                   'related_printers': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['skus'].label = "Skus: To add a sku, append the existing skus with a comma and enclose the new sku in inverted commas"
        self.fields['img_src'].label = "Image Source (a url)"
