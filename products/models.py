"""
Products Models

The models in this app are for 
Category - the category a product belongs to.
Supplies - inks, toners, parts etc...

"""
from django.db import models
from jsonfield import JSONField


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
    description = models.CharField(max_length=254, null=True, blank=True)
    relevant_model = models.CharField(max_length=60, default='Supplies')

    def __str__(self):
        return self.name


class Supplies(models.Model):
    """
    Supplies: Describes inks, toners, parts etc...
    """

    class Meta:
        verbose_name_plural = 'Supplies'

    skus = JSONField(null=True)
    name = models.CharField(max_length=60, null=True, blank=True)
    title = models.CharField(max_length=254, null=True, blank=True)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    img = models.CharField(max_length=254, blank=True, null=True)
    manufacturer = models.CharField(max_length=60, null=True, blank=True)
    description = models.TextField(null=True)
    blurb = models.TextField(null=True)
    related_printers = JSONField(null=True)
    features = JSONField(null=True)
    keywords = JSONField(null=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.name
