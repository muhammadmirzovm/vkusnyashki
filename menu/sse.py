import json
import asyncio

SUBSCRIBERS = {}

async def broadcast_event(data, event: str, monitor_id: int):
    """
    Pushes data to all subscribers of a specific monitor.
    """
    if monitor_id not in SUBSCRIBERS:
        return

    message = f"event: {event}\n"
    message += f"data: {json.dumps(data)}\n\n"


    dead_queues = []
    for queue in SUBSCRIBERS[monitor_id]:
        try:
            await queue.put(message)
        except Exception:
            dead_queues.append(queue)
    for q in dead_queues:
        SUBSCRIBERS[monitor_id].remove(q)
