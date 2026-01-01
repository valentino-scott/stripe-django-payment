import stripe
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages
from .models import PaymentRecord

# Configure Stripe with your test key
stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Home page with product listings"""
    products = [
        {
            'id': 'basic',
            'name': 'Basic Plan',
            'description': 'Get started with our basic features',
            'price': 9.99,
            'price_cents': 999,
            'currency': 'usd',
        },
        {
            'id': 'premium',
            'name': 'Premium Plan',
            'description': 'Access all premium features',
            'price': 29.99,
            'price_cents': 2999,
            'currency': 'usd',
        }
    ]
    
    return render(request, 'payments/home.html', {
        'products': products,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def create_checkout_session(request):
    """Create Stripe Checkout Session"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id', 'basic')
        
        # Get product details
        product_map = {
            'basic': {
                'name': 'Basic Plan', 
                'description': 'Get started with our basic features', 
                'price': 999, 
                'currency': 'usd'
            },
            'premium': {
                'name': 'Premium Plan', 
                'description': 'Access all premium features', 
                'price': 2999, 
                'currency': 'usd'
            }
        }
        
        product = product_map.get(product_id, product_map['basic'])
        
        # Get customer email from form or use a default for demo
        customer_email = request.POST.get('customer_email', 'test@example.com')
        
        try:
            # Create Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': product['currency'],
                            'product_data': {
                                'name': product['name'],
                                'description': product['description'],
                            },
                            'unit_amount': product['price'],
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_email=customer_email,
                success_url=request.build_absolute_uri(
                    reverse('payment_success')
                ) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
                metadata={
                    'product_id': product_id,
                    'product_name': product['name'],
                }
            )
            
            # Create payment record
            PaymentRecord.objects.create(
                stripe_checkout_id=checkout_session.id,
                customer_email=customer_email,
                product_name=product['name'],
                amount=product['price'],
                currency=product['currency'],
                status='pending'
            )
            
            return redirect(checkout_session.url)
            
        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe Error: {str(e)}")
            return render(request, 'payments/error.html', {'error': str(e)})
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'payments/error.html', {'error': str(e)})
    
    return redirect('home')

def payment_success(request):
    """Payment success page"""
    session_id = request.GET.get('session_id')
    
    context = {}
    if session_id:
        try:
            # Try to update payment record
            payment_record = PaymentRecord.objects.get(stripe_checkout_id=session_id)
            payment_record.status = 'completed'
            payment_record.save()
            
            context = {
                'payment_record': payment_record,
            }
            messages.success(request, 'Payment successful!')
        except PaymentRecord.DoesNotExist:
            context = {'error': 'Payment record not found'}
            messages.warning(request, 'Payment record not found')
        except Exception as e:
            context = {'error': f"Error: {str(e)}"}
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'payments/success.html', context)

def payment_cancel(request):
    """Payment cancellation page"""
    messages.info(request, 'Payment was cancelled. You can try again.')
    return render(request, 'payments/cancel.html')

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Update payment record
        try:
            payment_record = PaymentRecord.objects.get(stripe_checkout_id=session['id'])
            payment_record.status = 'completed'
            payment_record.stripe_payment_intent_id = session.get('payment_intent', '')
            payment_record.save()
            print(f"Webhook: Payment completed for {payment_record.customer_email}")
        except PaymentRecord.DoesNotExist:
            # Create new payment record if it doesn't exist
            PaymentRecord.objects.create(
                stripe_checkout_id=session['id'],
                customer_email=session.get('customer_details', {}).get('email', ''),
                product_name=session.get('metadata', {}).get('product_name', 'Unknown Product'),
                amount=session['amount_total'],
                currency=session['currency'],
                status='completed',
                stripe_payment_intent_id=session.get('payment_intent', '')
            )
    
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        
        try:
            payment_record = PaymentRecord.objects.get(stripe_checkout_id=session['id'])
            payment_record.status = 'canceled'
            payment_record.save()
        except PaymentRecord.DoesNotExist:
            pass
    
    return HttpResponse(status=200)

def payment_history(request):
    """View payment history"""
    payments = PaymentRecord.objects.all().order_by('-created_at')
    return render(request, 'payments/history.html', {'payments': payments})
