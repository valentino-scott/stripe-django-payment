from django.core.management.base import BaseCommand
from payments.models import DemoProduct

class Command(BaseCommand):
    help = 'Setup demo products for testing'

    def handle(self, *args, **options):
        products = [
            {
                'name': 'Basic Plan',
                'description': 'Get started with our basic features',
                'price': 999,
                'currency': 'usd',
            },
            {
                'name': 'Premium Plan',
                'description': 'Access all premium features',
                'price': 2999,
                'currency': 'usd',
            }
        ]
        
        for product_data in products:
            product, created = DemoProduct.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                self.stdout.write(f'Product already exists: {product.name}')