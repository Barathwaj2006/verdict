import os
import asyncio
from app.orchestration.investigation_controller import InvestigationController

async def run_integration():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable to run live tests.")
        return
        
    controller = InvestigationController(max_rounds=3)
    
    # We ask a very difficult, nuanced question to encourage the Lead to request a second round.
    objective = "Determine if Google's internal 'Antigravity' agent framework supports recursive research orchestration out of the box, or if it requires manual graph implementation."
    constraints = [
        "Find specific documentation or examples.",
        "Compare it to LangGraph's cyclic abilities."
    ]
    
    print(f"Starting Investigation: {objective}")
    
    final_verdict = await controller.run_investigation(objective, constraints)
    
    print("\n=======================================================")
    print("                    FINAL VERDICT                      ")
    print("=======================================================")
    print(f"Investigation ID: {final_verdict.investigation_id}")
    print(f"Rounds Completed: {final_verdict.research_rounds}")
    print(f"Termination Reason: {final_verdict.termination_reason}")
    print(f"Confidence: {final_verdict.confidence}\n")
    
    print("CONCLUSION:")
    print(final_verdict.conclusion)
    
    print("\nKEY FINDINGS:")
    for f in final_verdict.key_findings:
        print(f" - {f}")
        
    print("\nVERIFIED CLAIMS:")
    for c in final_verdict.verified_claims:
        print(f" [✓] {c}")
        
    print("\nCONTESTED CLAIMS:")
    for c in final_verdict.contested_claims:
        print(f" [⚠] {c}")
        
    print("\nUNRESOLVED QUESTIONS:")
    for q in final_verdict.unresolved_questions:
        print(f" [?] {q}")
        
    print(f"\nTotal Sources Examined: {final_verdict.source_count}")

if __name__ == "__main__":
    asyncio.run(run_integration())
