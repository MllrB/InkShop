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


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {'price': forms.HiddenInput(),
                   'related_printers': forms.HiddenInput()}
        fields = [
            'skus', 'title', 'category', 'img_src', 'image',
            'description', 'blurb', 'features', 'brochure',
            'published', 'related_printers', 'product_group',
            'vat_rate', 'cost_price', 'price',
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            placeholders = {
                'skus': 'Eg. ["sku1","sku2","sku3"]',
                'title': 'Text, Product Title',
                'img_src': 'Image Source, a URL',
                'description': 'Text, HTML friendly, avoid using css classes',
                'blurb': 'Text, HTML friendly, avoid using css classes',
                'features': 'Eg. [ { "feature_name": "Your text", \
                        "feature_value": "Your Value"}, { "feature_name": "Your text", "feature_value": "Your Value"}]',
                'brochure': 'Brochure Source, a URL',
            }

            fields_with_placholders = ['skus', 'title', 'img_src', 'description',
                                       'blurb', 'features', 'brochure', ]

            for field in self.fields:
                if field in fields_with_placholders:
                    self.fields[field].widget.attrs['placeholder'] = placeholder[field]
