import asyncio
import json

from django.http import StreamingHttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

from .models import Monitor, Category, Food

SUBSCRIBERS = {}


async def broadcast_event(data, monitor_id=None):
    """
    Push event to queues subscribed to this monitor_id.
    If monitor_id is None -> broadcast to all monitors.
    """
    if monitor_id is None:
        # broadcast to all
        for queues in list(SUBSCRIBERS.values()):
            for q in list(queues):
                await q.put(data)
    else:
        queues = SUBSCRIBERS.get(monitor_id, set())
        for q in list(queues):
            await q.put(data)


def monitor_page(request, pk):
    monitor = get_object_or_404(Monitor, pk=pk)
    categories = monitor.categories.prefetch_related("foods").all()

    data = []
    for c in categories:
        foods = []
        for f in c.foods.order_by("id"):
            if not f.is_available:
                continue
            photo_url = request.build_absolute_uri(f.photo.url) if f.photo else ""
            foods.append({
                "id": f.id,
                "name": f.name,
                "price": float(f.price),
                "description": f.description,
                "photo_url": photo_url,
                "is_available": f.is_available,
                "category_id": c.id,
            })
        data.append({"id": c.id, "name": c.name, "foods": foods})
    return render(request, "menu/monitor.html", {"monitor": monitor, "categories": data})


@require_GET
async def sse_monitor(request, monitor_pk):
    """
    SSE endpoint for a specific monitor (EventSource connects here).
    """

    try:
        monitor = await asyncio.to_thread(lambda: Monitor.objects.filter(pk=monitor_pk).exists())
    except Exception:
        raise Http404

    queue = asyncio.Queue()
    SUBSCRIBERS.setdefault(monitor_pk, set()).add(queue)

    async def event_stream():
        try:
            while True:
                data = await queue.get()

                yield f"data: {json.dumps(data)}\n\n".encode("utf-8")
        finally:

            subscribers = SUBSCRIBERS.get(monitor_pk)
            if subscribers and queue in subscribers:
                subscribers.remove(queue)
                if not subscribers:
                    SUBSCRIBERS.pop(monitor_pk, None)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
