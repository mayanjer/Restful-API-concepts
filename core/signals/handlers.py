from django.dispatch import receiver
from store.signals import create_order
from store.models import Order

@receiver(create_order)
def create_order_signal(sender, **kwargs):
    print(kwargs["order"])