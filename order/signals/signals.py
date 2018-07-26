from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from order.models import CbgOrders
@receiver(post_save, sender=CbgOrders)
def order_model_save_handler(sender, **kwargs):
    pass

@receiver(pre_save, sender=CbgOrders)
def order_model_pre_save_handler(sender, **kwargs):
    pass
