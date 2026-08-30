import asyncio
import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from sse_starlette.sse import EventSourceResponse

from app.api.dependencies import get_investigation_controller, get_firestore_repository
from app.orchestration.investigation_controller import InvestigationController
from app.services.firestore_repository import FirestoreRepository
from app.services.event_bus import event_bus
from app.models.events import EventType

router = APIRouter()

class StartInvestigationRequest(BaseModel):
    objective: str
    constraints: Optional[List[str]] = []

class StartInvestigationResponse(BaseModel):
    investigation_id: str
    status: str

async def run_investigation_background(investigation_id: str, objective: str, constraints: List[str], controller: InvestigationController):
    # Small hack: we need to pass investigation_id down.
    # The current controller creates its own investigation_id in `run_investigation`.
    # To keep contracts intact without changing run_investigation signature too much:
    try:
        # We will override the ID creation by generating it here, 
        # But controller.run_investigation does not take an ID.
        # Wait, let me check controller.run_investigation.
        pass
    except Exception as e:
        print(f"Background execution failed: {e}")

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "verdict-api"}

@router.post("/api/investigations", response_model=StartInvestigationResponse)
async def start_investigation(
    req: StartInvestigationRequest, 
    background_tasks: BackgroundTasks,
    controller: InvestigationController = Depends(get_investigation_controller)
):
    # To avoid changing the controller signature, we let controller create the ID and return it,
    # but controller's `run_investigation` returns FinalVerdict synchronously (async but blocking).
    # Since we must return ID immediately, we must decouple ID generation.
    
    investigation_id = f"inv_{uuid.uuid4().hex[:8]}"
    
    # We create investigation in Firestore immediately so status works.
    if controller.repository:
        controller.repository.create_investigation(investigation_id, req.objective, req.constraints)
        
    async def bg_task():
        try:
            # We must resume it since it's already created!
            await controller.resume_investigation(investigation_id)
        except Exception as e:
            print(f"Investigation failed: {e}")
            if controller.repository:
                controller.repository.update_investigation_status(investigation_id, "FAILED", termination_reason=str(e))
                
    background_tasks.add_task(bg_task)
    
    return StartInvestigationResponse(
        investigation_id=investigation_id,
        status="STARTED"
    )

@router.get("/api/investigations/{investigation_id}")
async def get_investigation_status(
    investigation_id: str,
    repository: FirestoreRepository = Depends(get_firestore_repository)
):
    meta = repository.get_investigation_metadata(investigation_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return meta

@router.get("/api/investigations/{investigation_id}/stream")
async def stream_investigation(
    request: Request,
    investigation_id: str,
    repository: FirestoreRepository = Depends(get_firestore_repository)
):
    meta = repository.get_investigation_metadata(investigation_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Investigation not found")

    async def event_generator():
        queue = await event_bus.subscribe_stream(investigation_id)
        try:
            while True:
                # If client closes connection
                if await request.is_disconnected():
                    break
                    
                try:
                    # Wait for next event
                    event = await asyncio.wait_for(queue.get(), timeout=1.0)
                    
                    # SSE format
                    data_str = json.dumps({
                        "investigation_id": event.investigation_id,
                        "timestamp": event.timestamp.isoformat(),
                        "event_type": event.event_type.value,
                        "round_number": event.round_number,
                        "agent": event.agent,
                        "payload": event.payload
                    })
                    
                    yield {
                        "event": event.event_type.value,
                        "data": data_str
                    }
                    
                    if event.event_type in [EventType.INVESTIGATION_COMPLETED, EventType.INVESTIGATION_FAILED]:
                        break
                except asyncio.TimeoutError:
                    # Keep connection alive
                    continue
        finally:
            event_bus.unsubscribe_stream(investigation_id, queue)
            
    return EventSourceResponse(event_generator())

@router.post("/api/investigations/{investigation_id}/resume", response_model=StartInvestigationResponse)
async def resume_investigation(
    investigation_id: str,
    background_tasks: BackgroundTasks,
    controller: InvestigationController = Depends(get_investigation_controller)
):
    if not controller.repository:
        raise HTTPException(status_code=500, detail="Persistence not configured")
        
    meta = controller.repository.get_investigation_metadata(investigation_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    if meta.get("status") in ["COMPLETED", "FAILED"]:
        raise HTTPException(status_code=400, detail="Investigation already finished")
        
    async def bg_task():
        try:
            await controller.resume_investigation(investigation_id)
        except Exception as e:
            print(f"Investigation failed to resume: {e}")
            controller.repository.update_investigation_status(investigation_id, "FAILED", termination_reason=str(e))
            
    background_tasks.add_task(bg_task)
    
    return StartInvestigationResponse(
        investigation_id=investigation_id,
        status="RESUMED"
    )

@router.get("/api/investigations/{investigation_id}/verdict")
async def get_verdict(
    investigation_id: str,
    repository: FirestoreRepository = Depends(get_firestore_repository)
):
    meta = repository.get_investigation_metadata(investigation_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    if "final_verdict" not in meta:
        raise HTTPException(status_code=404, detail="Verdict not available yet")
        
    return meta["final_verdict"]
