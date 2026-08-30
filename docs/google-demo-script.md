# VERDICT: Demo Video Script (Google Hackathon)

**Target Length:** 3:00 Max

### 00:00–00:20: The Problem
*(Visual: Standard ChatGPT or Gemini chat window giving a fast but generic answer to a complex business question.)*
**Voiceover:** Generative AI is incredible at answering questions. But when you need to make a critical business decision, you don't just need an answer. You need an investigation. Standard models summarize, but they don't research, challenge, or verify. That's why we built VERDICT.

### 00:20–00:40: VERDICT Concept
*(Visual: Cut to VERDICT Presentation Website, scrolling smoothly through the Agent roles: Lead, Specialist, Skeptic, Verifier.)*
**Voiceover:** VERDICT is an autonomous decision-research engine powered by Google Gemini. It doesn't just generate text; it orchestrates a dynamic team of AI agents that research in parallel, adversarially challenge evidence, and recursively hunt for the truth.

### 00:40–01:15: User Starts Investigation
*(Visual: Cut to the VERDICT dark-mode UI. User types: "Should our startup adopt Rust or Go for our new microservices? Team size: 5. Timeline: Q3." User clicks Start.)*
**Voiceover:** Let's ask a complex architectural question. Behind the scenes, the FastAPI backend receives the request. The Lead Agent, powered by `gemini-3.7-flash` and the Google GenAI SDK, structures a research plan. It dynamically spawns Specialist Researchers to scour the web.

### 01:15–01:45: Dynamic Agents + Research
*(Visual: The 3D UI comes alive. Nodes branch out. Live SSE telemetry streams in the sidebar showing "Researcher 1 scraping X", "Researcher 2 scraping Y".)*
**Voiceover:** Here, you see real-time Server-Sent Events. These researchers are retrieving actual web data. Crucially, a strict Python-level Evidence Integrity module ensures that if Gemini hallucinates a source URL, it is instantly rejected. Only verified external data enters the system.

### 01:45–02:10: Skeptic + Verifier
*(Visual: The UI flashes yellow/orange as the "Skeptic" node pulses. Then the "Verifier" node activates.)*
**Voiceover:** This is the core innovation. Once evidence is gathered, the Skeptic agent analyzes it specifically looking for logical flaws, bias, or unsupported claims. It flags a claim about Rust's learning curve. The Verifier agent then executes an independent search strictly to prove or disprove the Skeptic's challenge.

### 02:10–02:35: Knowledge Gap / Recursion
*(Visual: UI shows "Round 1 Complete. Knowledge Gap Identified: Need more data on compilation times. Initiating Round 2.")*
**Voiceover:** The Lead Agent evaluates the verified evidence matrix. It realizes it doesn't have enough data on compilation times. Instead of guessing, VERDICT loops. It creates a targeted Round 2 mission. All of this state is durably persisted in Google Cloud Firestore.

### 02:35–02:50: Final Verdict
*(Visual: The 3D graph settles. The "Executive Briefing" UI appears, showing clear tabs for Recommendation, Verified Facts, Contested Claims, and Trade-offs.)*
**Voiceover:** Once the evidence threshold is met, VERDICT delivers the final report. Not a chatbot summary, but a structured, verified, and transparent executive briefing.

### 02:50–03:00: Google Technology + Closing
*(Visual: Show the Architecture Diagram highlighting Gemini, GenAI SDK, Firestore, Cloud Run.)*
**Voiceover:** Built entirely on Google Cloud using Gemini 3.7 Flash, Firestore, and the GenAI SDK, VERDICT moves AI from generating text to conducting actual investigations. Thank you.
