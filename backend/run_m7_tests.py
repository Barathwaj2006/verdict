import os
import asyncio
import httpx
from httpx_sse import connect_sse

async def run_m7_demo():
    print("========================================")
    print("VERDICT M7: API + LIVE STREAMING DEMO")
    print("========================================")
    
    # We will spin up the uvicorn server in a subprocess to test it against real HTTP
    import subprocess
    import time
    
    # Set env vars to ensure we use emulator if set, etc.
    env = os.environ.copy()
    env["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
    env["GOOGLE_CLOUD_PROJECT"] = "demo-project"
    
    print("Starting FastAPI server in background...")
    server = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8005"],
        env=env,
        cwd="backend"
    )
    
    try:
        # Wait for server to boot
        await asyncio.sleep(3)
        
        async with httpx.AsyncClient(base_url="http://127.0.0.1:8005") as client:
            # 1. Start investigation
            print("\n[✓] POST /api/investigations")
            resp = await client.post("/api/investigations", json={
                "objective": "Determine who created C++",
                "constraints": []
            })
            resp.raise_for_status()
            data = resp.json()
            inv_id = data["investigation_id"]
            print(f"Investigation started! ID: {inv_id}")
            
            # 2. Subscribe to SSE
            print(f"\n[✓] GET /api/investigations/{inv_id}/stream (SSE)")
            
            # We connect to SSE and wait for INVESTIGATION_COMPLETED
            async with connect_sse(client, "GET", f"/api/investigations/{inv_id}/stream", timeout=60.0) as event_source:
                async for sse in event_source.aiter_sse():
                    print(f"[STREAM] {sse.event}")
                    if sse.event in ["INVESTIGATION_COMPLETED", "INVESTIGATION_FAILED"]:
                        break
            
            # 3. Get Final Verdict
            print(f"\n[✓] GET /api/investigations/{inv_id}/verdict")
            resp = await client.get(f"/api/investigations/{inv_id}/verdict")
            
            # Depending on if we had an API key, we might have a verdict
            if resp.status_code == 200:
                print(f"Verdict retrieved: {resp.json().get('termination_reason')}")
            else:
                print(f"Verdict not found: {resp.status_code}")
                
        print("\n========================================")
        print("DEMO COMPLETE")
        print("========================================")

    finally:
        server.terminate()
        server.wait()

if __name__ == "__main__":
    asyncio.run(run_m7_demo())
