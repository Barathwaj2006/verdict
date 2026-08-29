import os
import asyncio
from app.agents.lead.agent import LeadAgent
from app.orchestration.research_orchestrator import ResearchOrchestrator
from app.agents.skeptic.agent import SkepticAgent
from app.agents.verifier.agent import VerifierAgent

async def run_integration():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable to run live tests.")
        return
        
    lead = LeadAgent()
    orchestrator = ResearchOrchestrator()
    skeptic = SkepticAgent()
    verifier = VerifierAgent()
    
    objective = "Find existing implementations of autonomous multi-agent research systems and determine whether this architecture is already common."
    constraints = []
    
    print("--- 1. LEAD AGENT PLANNING ---")
    plan = lead.create_plan(objective, constraints)
    
    print("\n--- 2. RESEARCH ORCHESTRATOR EXECUTING ---")
    batch = await orchestrator.execute_plan(plan, "inv_test_40", 1)
    
    print("\n--- 3. SKEPTIC AGENT EXECUTING ---")
    report = await skeptic.evaluate_batch(batch, plan)
    
    print("\n--- 4. VERIFIER AGENT EXECUTING ---")
    verifications = await verifier.verify_batch(batch, report, plan)
    
    print("\n--- 5. FINAL RESULTS ---")
    for v in verifications:
        print(f"\n[Claim: {v.original_claim}]")
        print(f"Status: {v.verification_status}")
        print(f"Summary: {v.evidence_summary}")
        print("Evidence Matrix:")
        for entry in v.evidence_matrix:
            print(f"  - {entry.source_url}: {entry.relationship} (Relevance: {entry.relevance})")
        print(f"Unresolved: {v.unresolved_questions}")

if __name__ == "__main__":
    asyncio.run(run_integration())
