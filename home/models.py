""" 
Content Management Model to store information for the site's 
information pages and recommended products
"""
from django.db import models

from products.models import Product


class ContentManagement(models.Model):

    name = models.CharField(max_length=254, null=False, blank=False)
    active = models.BooleanField(default=False)
    about = models.TextField(null=True, blank=True)
    delivery = models.TextField(null=True, blank=True)
    questions = models.TextField(null=True, blank=True)
    terms = models.TextField(null=True, blank=True)
    privacy = models.TextField(null=True, blank=True)
    staff_pick1 = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='pick1')
    staff_pick2 = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='pick2')
    staff_pick3 = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='pick3')
