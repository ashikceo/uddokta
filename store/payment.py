import json
import hashlib
import requests
from django.conf import settings
from django.urls import reverse
from .models import Order


def generate_transaction_id(order_id):
    return f'UD{order_id:06d}{hashlib.md5(str(order_id).encode()).hexdigest()[:6].upper()}'


def sslcommerz_init(order, request):
    tran_id = generate_transaction_id(order.id)
    order.tracking_id = tran_id
    order.save(update_fields=['tracking_id'])

    post_data = {
        'store_id': settings.SSLCOMMERZ_STORE_ID,
        'store_passwd': settings.SSLCOMMERZ_STORE_PASS,
        'total_amount': str(order.total),
        'currency': 'BDT',
        'tran_id': tran_id,
        'success_url': request.build_absolute_uri(reverse('payment_success', args=[order.id])),
        'fail_url': request.build_absolute_uri(reverse('payment_fail', args=[order.id])),
        'cancel_url': request.build_absolute_uri(reverse('payment_cancel', args=[order.id])),
        'cus_name': order.name,
        'cus_phone': order.phone,
        'cus_add1': order.address[:100] if order.address else 'N/A',
        'cus_city': 'Dhaka',
        'cus_country': 'Bangladesh',
        'shipping_method': 'Courier',
        'product_name': f'Order #{order.id}',
        'product_category': 'General',
        'product_profile': 'general',
    }

    try:
        response = requests.post(settings.SSLCOMMERZ_API_URL, data=post_data, timeout=30)
        result = response.json()
        if result.get('status') == 'SUCCESS':
            return result['GatewayPageURL']
        return None
    except requests.RequestException:
        return None


def sslcommerz_validate(order):
    tran_id = order.tracking_id
    if not tran_id:
        return False

    validation_url = f'{settings.SSLCOMMERZ_API_VALIDATION}?store_id={settings.SSLCOMMERZ_STORE_ID}&store_passwd={settings.SSLCOMMERZ_STORE_PASS}&tran_id={tran_id}'

    try:
        response = requests.get(validation_url, timeout=30)
        result = response.json()
        if result.get('status') == 'VALID' or result.get('status') == 'VALIDATED':
            return True
        return False
    except requests.RequestException:
        return False
