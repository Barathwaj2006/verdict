import asyncio
import inspect
from typing import Callable, List, Any, Dict, Set
from app.models.events import StreamingEvent

class EventBus:
    def __init__(self):
        self._subscribers: List[Callable[[StreamingEvent], Any]] = []
        self._stream_queues: Dict[str, Set[asyncio.Queue]] = {}

    def subscribe(self, callback: Callable[[StreamingEvent], Any]):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[StreamingEvent], Any]):
        if callback in self._subscribers:
            self._subscribers.remove(callback)
            
    async def subscribe_stream(self, investigation_id: str) -> asyncio.Queue:
        if investigation_id not in self._stream_queues:
            self._stream_queues[investigation_id] = set()
            
        queue = asyncio.Queue()
        self._stream_queues[investigation_id].add(queue)
        return queue
        
    def unsubscribe_stream(self, investigation_id: str, queue: asyncio.Queue):
        if investigation_id in self._stream_queues and queue in self._stream_queues[investigation_id]:
            self._stream_queues[investigation_id].remove(queue)
            if not self._stream_queues[investigation_id]:
                del self._stream_queues[investigation_id]

    def publish(self, event: StreamingEvent):
        # Fire-and-forget logic so subscribers do not block or crash the main investigation loop.
        for callback in self._subscribers:
            try:
                # If callback is async, create a task
                if inspect.iscoroutinefunction(callback):
                    asyncio.create_task(self._safe_async_call(callback, event))
                else:
                    # If synchronous, run it in executor or safely catch errors
                    try:
                        callback(event)
                    except Exception as e:
                        print(f"EventBus subscriber {callback} failed: {e}")
            except Exception as e:
                print(f"EventBus dispatch error: {e}")
                
        # Publish to stream queues
        if event.investigation_id in self._stream_queues:
            for queue in list(self._stream_queues[event.investigation_id]):
                try:
                    queue.put_nowait(event)
                except Exception as e:
                    print(f"Failed to put event in queue: {e}")

    async def _safe_async_call(self, callback, event):
        try:
            await callback(event)
        except Exception as e:
            print(f"EventBus async subscriber {callback} failed: {e}")

# Global instance for ease of use
event_bus = EventBus()
