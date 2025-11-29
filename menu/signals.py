import asyncio

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Food
from .views import broadcast_event


def _get_monitor_id_from_food(instance):
    try:
        return instance.category.monitor_id
    except Exception:
        return None


@receiver(post_save, sender=Food)
def food_saved(sender, instance, created, **kwargs):
    monitor_id = _get_monitor_id_from_food(instance)
    event = {
        "type": "food_update",
        "action": "created" if created else "updated",
        "payload": {
            "id": instance.id,
            "name": instance.name,
            "price": float(instance.price),
            "is_available": instance.is_available,
            "description": instance.description,
            "photo_url": instance.photo.url if instance.photo else "",
            "category_id": instance.category_id,
            "monitor_id": monitor_id,
        },
    }
    try:
        asyncio.get_event_loop().create_task(broadcast_event(event, monitor_id=monitor_id))
    except RuntimeError:
        from asgiref.sync import async_to_sync
        async_to_sync(broadcast_event)(event, monitor_id=monitor_id)



@receiver(post_delete, sender=Food)
def food_deleted(sender, instance, **kwargs):
    """
    Triggered on delete
    """
    monitor_id = _get_monitor_id_from_food(instance)
    event = {"type": "food_update", "action": "deleted", "payload": {"id": instance.id, "category_id": instance.category_id}}
    try:
        asyncio.get_event_loop().create_task(broadcast_event(event, monitor_id=monitor_id))
    except RuntimeError:
        from asgiref.sync import async_to_sync

        async_to_sync(broadcast_event)(event, monitor_id=monitor_id)

