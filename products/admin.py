from django.contrib import admin
from .models import Category, Product, VatGroup, ProductGroup


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductGroup)
admin.site.register(VatGroup)
