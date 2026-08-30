import os
import asyncio
from app.orchestration.investigation_controller import InvestigationController
from app.services.event_bus import event_bus

def print_event(evt):
    print(f"[{evt.timestamp.strftime('%H:%M:%S')}] [EVENT] {evt.event_type.value} | Inv: {evt.investigation_id} | Round: {evt.round_number} | Payload: {evt.payload}")

async def run_integration():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable to run live tests.")
        return
        
    event_bus.subscribe(print_event)
    controller = InvestigationController(max_rounds=2)
    
    objective = "Determine the creator of Python. Then specifically ask who created C++."
    constraints = []
    
    print("\nStarting M5.5 Investigation with Event Streaming...\n")
    final_verdict = await controller.run_investigation(objective, constraints)
    
    print("\n=======================================================")
    print("                    FINAL VERDICT                      ")
    print("=======================================================")
    print(f"Rounds: {final_verdict.research_rounds}")
    print(f"Termination: {final_verdict.termination_reason}")
    print(f"Sources Examined: {final_verdict.source_count}")
    print("\nCONCLUSION:")
    print(final_verdict.conclusion)

if __name__ == "__main__":
    asyncio.run(run_integration())
