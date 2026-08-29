import os
import asyncio
from app.orchestration.investigation_controller import InvestigationController
from app.services.event_bus import event_bus
from app.services.firestore_repository import FirestoreRepository

def print_event(evt):
    print(f"[{evt.timestamp.strftime('%H:%M:%S')}] [EVENT] {evt.event_type.value} | Inv: {evt.investigation_id} | Round: {evt.round_number} | Payload: {evt.payload}")

async def run_integration():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable to run live tests.")
        return
        
    print("========================================")
    print("VERDICT — FIRESTORE PERSISTENCE DEMO")
    print("========================================")
    
    # We use local firestore emulator if set, otherwise real cloud
    os.environ.setdefault("FIRESTORE_EMULATOR_HOST", "127.0.0.1:8080")
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "demo-project")
    
    event_bus.subscribe(print_event)
    repo = FirestoreRepository()
    
    controller = InvestigationController(max_rounds=1, repository=repo)
    
    objective = "Determine who created C++"
    
    print("\n[✓] Creating and running Investigation (Round 1 only)\n")
    # For demonstration, we'll manually step through or run 1 round
    final_verdict = await controller.run_investigation(objective, [])
    
    if final_verdict:
        investigation_id = final_verdict.investigation_id
        
        print("\n--- SIMULATED PROCESS INTERRUPTION ---\n")
        
        print(f"[✓] Reloading Investigation {investigation_id} from Firestore")
        
        # New controller instance
        controller2 = InvestigationController(max_rounds=2, repository=repo)
        
        print("[✓] Resuming investigation (should run Round 2 and finalize)")
        resumed_verdict = await controller2.resume_investigation(investigation_id)
        
        print("\n========================================")
        print("INVESTIGATION COMPLETE")
        print("========================================")
        print(f"Rounds: {resumed_verdict.research_rounds}")
        print(f"Termination: {resumed_verdict.termination_reason}")
        print(f"Persistence: FIRESTORE")
        print("\nCONCLUSION:")
        print(resumed_verdict.conclusion)
        print("========================================")

if __name__ == "__main__":
    asyncio.run(run_integration())
