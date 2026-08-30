# VERDICT: Autonomous Decision-Research Engine

## Inspiration
Generative AI excels at answering questions, but real-world decision-making requires investigation. Whether a team is evaluating an architecture migration, a legal claim, or a competitive threat, standard LLMs often hallucinate, summarize poorly, or stop at surface-level answers. We built VERDICT because critical decisions demand evidence, adversarial challenge, independent verification, and recursive research—not just a single generative pass.

## What it does
VERDICT is an autonomous, multi-agent investigation system that mimics a real-world research team. 
When given a complex problem and constraints:
1. **The Lead Agent** breaks the problem into a strategic research plan.
2. **Specialist Researchers** are dynamically spawned to scrape the web and extract evidence in parallel.
3. **The Skeptic** adversarially challenges the extracted claims, looking for logical flaws or unsupported statements.
4. **The Verifier** runs independent secondary searches to confirm or refute the Skeptic's challenges.
5. **The Lead Agent** evaluates the verified matrix. If knowledge gaps remain, it loops back and spawns a new round of research.
Once the evidence threshold is met, it issues a final, highly structured "Verdict" detailing verified facts, contested claims, and actionable recommendations.

## How we built it
VERDICT is powered by a modern, event-driven Google Cloud stack:
- **Core AI:** Google `gemini-3.7-flash` via the official `google-genai` SDK.
- **Agent Architecture:** Pure Python FastAPI backend orchestrating dynamic agents using Gemini's native structured outputs (`response_schema`).
- **State & Memory:** Google Cloud Firestore acts as the persistence layer, durably storing round histories and evidence matrices.
- **Real-Time Telemetry:** `sse-starlette` broadcasts backend agent activity (EventBus) to the client.
- **Frontend:** A Next.js 14 App Router application with Tailwind CSS and React Three Fiber (R3F) for interactive 3D investigation visualization.

## Challenges we ran into
- **Hallucination Control:** Early iterations accepted hallucinated sources. We built a strict Python-level Evidence Integrity module that actively rejects any URL not retrieved by the actual search provider, forcing the agents to rely strictly on real-world data.
- **Agent Loops:** Multi-agent systems tend to loop infinitely or stop too early. We solved this by making the Lead Agent the sole arbiter of "Evidence Sufficiency", enforcing strict round-limits and deduplicating queries.
- **State Synchronization:** Sending complex multi-agent state to a React frontend in real-time required a robust EventBus and SSE architecture to prevent race conditions.

## Accomplishments that we're proud of
- **True Recursion:** The system dynamically identifies its own knowledge gaps and initiates subsequent research rounds autonomously.
- **Adversarial Design:** The Skeptic and Verifier agents fundamentally alter the output quality by forcing the system to doubt its own findings.
- **Premium UX:** Moving away from standard "chatbot" interfaces to a telemetry-driven Command Center with 3D visualization and a beautiful 2D fallback.

## What we learned
- Structured outputs natively provided by the Google GenAI SDK are vastly superior to prompt-engineering JSON formats.
- Real-world decision engines need discrete "Challenge" phases. Without a Skeptic, LLMs suffer from severe confirmation bias.

## What's next for VERDICT
- **Integration with Google Workspace:** Allowing VERDICT to cite internal Google Drive documents.
- **Long-running Investigations:** Converting the fast SSE loop into a background Cloud Run job for investigations that run for hours.
- **Live Deployment:** Finalizing the Cloud Run CI/CD pipeline once our Google Cloud billing activation is processed.
