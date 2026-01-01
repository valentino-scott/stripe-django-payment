from django.contrib import admin
from .models import DemoProduct, PaymentRecord

@admin.register(DemoProduct)
class DemoProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'is_active']
    list_filter = ['is_active', 'currency']
    search_fields = ['name', 'description']

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ['customer_email', 'product_name', 'amount_display', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['customer_email', 'product_name', 'stripe_checkout_id']
    readonly_fields = ['created_at', 'updated_at']
    
    def amount_display(self, obj):
        return f"${obj.amount/100:.2f}"
    amount_display.short_description = 'Amount'