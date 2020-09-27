from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            if product.img_src == '':
                product.img_src = None
                product.save()
