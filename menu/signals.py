import asyncio

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Food
from .views import broadcast_event


@receiver(post_save, sender=Food)
def food_saved(sender, instance, created, **kwargs):
    """
    Triggered on create or update
    """
    event = {
        "type": "food_update",
        "action": "created" if created else "updated",
        "payload": {
            "id": instance.id,
            "name": instance.name,
            "price": float(instance.price),
            "is_available": instance.is_available,
            "description": instance.description,
            "photo": instance.photo.url if instance.photo else "",
        },
    }
    try:
        asyncio.get_event_loop().create_task(broadcast_event(event))
    except RuntimeError:
        from asgiref.sync import async_to_sync

        async_to_sync(broadcast_event)(event)


@receiver(post_delete, sender=Food)
def food_deleted(sender, instance, **kwargs):
    """
    Triggered on delete
    """
    event = {"type": "food_update", "action": "deleted", "payload": {"id": instance.id}}
    try:
        asyncio.get_event_loop().create_task(broadcast_event(event))
    except RuntimeError:
        from asgiref.sync import async_to_sync

        async_to_sync(broadcast_event)(event)
