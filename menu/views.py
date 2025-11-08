import asyncio
import json
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_GET
from .models import Food

SUBSCRIBERS = set()

async def broadcast_event(data):
    """
    Send an event to all connected SSE clients
    """
    for queue in list(SUBSCRIBERS):
        await queue.put(data)


def menu_page(request):
    """
    Render the menu page with only available food items
    """
    foods = []
    for f in Food.objects.filter(is_available=True): 
        foods.append({
            "id": f.id,
            "name": f.name,
            "price": float(f.price),
            "is_available": f.is_available,
            "description": f.description,
            "photo": f.photo.url if f.photo else "",
        })
    return render(request, "menu/index.html", {"foods": foods})

@require_GET
async def sse_menu(request):
    """
    Server-Sent Events endpoint to push real-time updates
    """
    queue = asyncio.Queue()
    SUBSCRIBERS.add(queue)

    async def event_stream():
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n".encode("utf-8")
        finally:
            SUBSCRIBERS.remove(queue)

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no" 
    return response
