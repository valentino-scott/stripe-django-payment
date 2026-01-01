from django.db import models
from django.conf import settings

class DemoProduct(models.Model):
    """Demo products for testing Stripe"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    stripe_price_id = models.CharField(max_length=100, blank=True)  # For real integration
    price = models.IntegerField()  # Price in cents
    currency = models.CharField(max_length=3, default='usd')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price/100:.2f}"

class PaymentRecord(models.Model):
    """Record payments for demo purposes"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]
    
    stripe_checkout_id = models.CharField(max_length=100, unique=True)
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    customer_email = models.EmailField()
    product_name = models.CharField(max_length=200)
    amount = models.IntegerField()  # Amount in cents
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.customer_email} - ${self.amount/100:.2f}"