"""
Products Models

The models in this app are for 
Category - the category a product belongs to.
Supplies - inks, toners, parts etc...

"""
from django.db import models
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """
    Categories
    Required: 
        1. name - the programmatic category name
        2. relevant_model - the product model that the category contains
    """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    img = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    relevant_model = models.CharField(max_length=60, default='supplies')

    def __str__(self):
        return self.friendly_name


class ProductGroup(models.Model):
    """
    ProductGroup to allow products to be sold for differing profit margins
    """
    name = models.CharField(max_length=50)
    profit_margin = models.IntegerField(
        default=30, validators=[MaxValueValidator(99), MinValueValidator(1)])

    def __str__(self):
        return self.name


class VatGroup(models.Model):
    """
    VatGroup: A model to allow for variable VAT/TAX rates to be applied
    """
    name = models.CharField(max_length=50)
    vat_rate = models.IntegerField(
        default=21, validators=[MaxValueValidator(99), MinValueValidator(0)])

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Supplies: Describes inks, toners, parts etc...
    """

    class Meta:
        verbose_name_plural = 'Products'

    skus = JSONField(null=True)
    title = models.CharField(max_length=254, null=True, blank=True)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    img_src = models.CharField(max_length=254, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    blurb = models.TextField(null=True, blank=True)
    features = JSONField(null=True, blank=True)
    published = models.BooleanField(default=True)
    related_printers = JSONField(null=True, blank=True)
    brochure = models.CharField(max_length=254, null=True, blank=True)
    product_group = models.ForeignKey(
        'ProductGroup', null=True, blank=True, default=1, on_delete=models.SET_NULL)
    vat_rate = models.ForeignKey(
        'VatGroup', null=True, blank=True,  default=1, on_delete=models.SET_NULL)
    cost_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __init__(self, *args, **kwargs):
        """
        Overide init to populate price fields
        """
        super(Product, self).__init__(*args, **kwargs)

        self.price = self.calculate_price()
        self.save()

    def __str__(self):
        return self.title

    def calculate_price(self):
        margin = (100 - Decimal(self.product_group.profit_margin))/100
        price = Decimal(self.cost_price) / Decimal(margin)
        return round(price, 2)

    def calculate_vat(self):
        vat_rate = (Decimal(self.vat_rate.vat_rate) + 100)/100
        vat = (Decimal(self.price) * vat_rate) - Decimal(self.price)
        return round(vat, 2)

    def calculate_inc_vat_price(self):
        inc_vat_price = Decimal(self.price) * \
            ((Decimal(self.vat_rate.vat_rate) + 100)/100)
        return round(inc_vat_price, 2)
