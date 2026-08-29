import asyncio
from typing import Callable, List, Any
from app.models.events import StreamingEvent

class EventBus:
    def __init__(self):
        self._subscribers: List[Callable[[StreamingEvent], Any]] = []

    def subscribe(self, callback: Callable[[StreamingEvent], Any]):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[StreamingEvent], Any]):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def publish(self, event: StreamingEvent):
        # Fire-and-forget logic so subscribers do not block or crash the main investigation loop.
        for callback in self._subscribers:
            try:
                # If callback is async, create a task
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(self._safe_async_call(callback, event))
                else:
                    # If synchronous, run it in executor or safely catch errors
                    try:
                        callback(event)
                    except Exception as e:
                        print(f"EventBus subscriber {callback} failed: {e}")
            except Exception as e:
                print(f"EventBus dispatch error: {e}")

    async def _safe_async_call(self, callback, event):
        try:
            await callback(event)
        except Exception as e:
            print(f"EventBus async subscriber {callback} failed: {e}")

# Global instance for ease of use
event_bus = EventBus()
