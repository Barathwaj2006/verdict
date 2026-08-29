import os
import json
from app.agents.lead.agent import LeadAgent

def run_scenarios():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable.")
        return
        
    agent = LeadAgent()
    
    scenarios = [
        {
            "name": "Scenario 1: Clear Hackathon Request",
            "objective": "Find me a winning idea for this hackathon: https://devpost.com/software. I want to use Google GenAI APIs.",
            "constraints": ["Solo developer", "3 days to build"]
        },
        {
            "name": "Scenario 2: Ambiguous Request",
            "objective": "Help me build an app.",
            "constraints": []
        },
        {
            "name": "Scenario 3: Different Objective",
            "objective": "Determine whether we should migrate our backend from Node.js to Python/FastAPI.",
            "constraints": ["Current team only knows JS", "We need high performance for ML tasks"]
        }
    ]
    
    for s in scenarios:
        print(f"--- {s['name']} ---")
        print(f"Objective: {s['objective']}")
        print(f"Constraints: {s['constraints']}")
        try:
            plan = agent.create_plan(s['objective'], s['constraints'])
            print("\nOutput Plan (JSON):")
            print(plan.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error: {e}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    run_scenarios()
