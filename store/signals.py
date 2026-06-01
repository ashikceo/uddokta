from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification, WithdrawalRequest, RefundRequest, Product, ProductColorVariant, ProductSizeVariant
from .tasks import send_order_confirmation_email


@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    if created and instance.user:
        Notification.objects.create(
            user=instance.user,
            type='order_placed',
            title=f'Order #{instance.id} placed successfully',
            message=f'Your order of ৳{instance.total} has been placed.',
            link='/dashboard/',
        )
        send_order_confirmation_email.delay(instance.id)
    if instance.status == 'completed':
        partners = set()
        for item in instance.items.all():
            if item.product and item.product.partner and item.product.partner.user:
                partner_user = item.product.partner.user
                Notification.objects.create(
                    user=partner_user,
                    type='order_status',
                    title=f'Order #{instance.id} completed',
                    message='Wallet has been credited.',
                    link='/dashboard/wallet/',
                )


@receiver(post_save, sender=WithdrawalRequest)
def withdrawal_notification(sender, instance, created, **kwargs):
    if instance.partner and instance.partner.user:
        if instance.status == 'approved':
            Notification.objects.create(
                user=instance.partner.user,
                type='withdrawal_status',
                title=f'Withdrawal #{instance.id} approved',
                message=f'৳{instance.net_amount} will be sent to your account shortly.',
                link='/dashboard/wallet/withdrawals/',
            )
        elif instance.status == 'rejected':
            Notification.objects.create(
                user=instance.partner.user,
                type='withdrawal_status',
                title=f'Withdrawal #{instance.id} rejected',
                message=instance.admin_notes or 'Please contact support for details.',
                link='/dashboard/wallet/withdrawals/',
            )


@receiver(post_save, sender=RefundRequest)
def refund_notification(sender, instance, created, **kwargs):
    if instance.user:
        if instance.status == 'approved':
            Notification.objects.create(
                user=instance.user,
                type='wallet_credit',
                title=f'Refund #{instance.id} approved',
                message=f'৳{instance.amount} has been refunded.',
                link='/dashboard/',
            )
        elif instance.status == 'rejected':
            Notification.objects.create(
                user=instance.user,
                type='wallet_credit',
                title=f'Refund #{instance.id} rejected',
                message=instance.admin_notes or 'Your refund request was not approved.',
                link='/dashboard/refunds/',
            )


@receiver(post_save, sender=Product)
def low_stock_alert(sender, instance, **kwargs):
    if instance.stock <= instance.low_stock_threshold and instance.partner and instance.partner.user:
        existing = Notification.objects.filter(
            partner=instance.partner,
            type='low_stock',
            title__contains=instance.name,
            is_read=False,
        ).exists()
        if not existing:
            Notification.objects.create(
                user=instance.partner.user,
                partner=instance.partner,
                type='low_stock',
                title=f'Low Stock: {instance.name}',
                message=f'Only {instance.stock} left (threshold: {instance.low_stock_threshold}). Restock soon!',
                link='/dashboard/products/',
            )


@receiver(post_save, sender=ProductColorVariant)
@receiver(post_save, sender=ProductSizeVariant)
def variant_low_stock_alert(sender, instance, **kwargs):
    if instance.stock > 0 and instance.stock <= instance.product.low_stock_threshold and instance.product.partner and instance.product.partner.user:
        existing = Notification.objects.filter(
            partner=instance.product.partner,
            type='low_stock',
            title__contains=instance.product.name,
            is_read=False,
        ).exists()
        if not existing:
            Notification.objects.create(
                user=instance.product.partner.user,
                partner=instance.product.partner,
                type='low_stock',
                title=f'Low Stock: {instance.product.name} ({instance.color_name if sender == ProductColorVariant else instance.size_name})',
                message=f'Only {instance.stock} of {instance.color_name if sender == ProductColorVariant else instance.size_name} left (threshold: {instance.product.low_stock_threshold}).',
                link='/dashboard/products/',
            )
