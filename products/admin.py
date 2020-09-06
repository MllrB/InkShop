from django.contrib import admin
from .models import Category, Supplies, VatGroup, ProductGroup


admin.site.register(Category)
admin.site.register(Supplies)
admin.site.register(ProductGroup)
admin.site.register(VatGroup)
