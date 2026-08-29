import os
import asyncio
from app.agents.lead.agent import LeadAgent
from app.orchestration.research_orchestrator import ResearchOrchestrator
from app.agents.skeptic.agent import SkepticAgent

async def run_integration():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable to run live tests.")
        return
        
    lead = LeadAgent()
    orchestrator = ResearchOrchestrator()
    skeptic = SkepticAgent()
    
    objective = "Find existing implementations of autonomous multi-agent research systems and determine whether this architecture is already common."
    constraints = []
    
    print("--- 1. LEAD AGENT PLANNING ---")
    plan = lead.create_plan(objective, constraints)
    
    print("\n--- 2. RESEARCH ORCHESTRATOR EXECUTING ---")
    batch = await orchestrator.execute_plan(plan, "inv_test_30", 1)
    
    print("\n--- 3. SKEPTIC AGENT EXECUTING ---")
    report = await skeptic.evaluate_batch(batch, plan)
    
    print("\n--- 4. SKEPTIC RESULTS ---")
    print(f"Total Claims Analyzed: {len(report.challenges)}")
    
    for chal in report.challenges:
        print(f"\n[Claim: {chal.original_claim}]")
        print(f"Severity: {chal.severity}")
        print(f"Type: {chal.challenge_type}")
        print(f"Question: {chal.challenge_question}")
        print(f"Counter Evidence: {chal.counter_evidence}")
        print(f"Disposition: {chal.disposition}")
        print(f"Counter Sources: {chal.counter_sources}")

if __name__ == "__main__":
    asyncio.run(run_integration())
