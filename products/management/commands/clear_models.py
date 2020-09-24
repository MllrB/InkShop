from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.all().delete()
