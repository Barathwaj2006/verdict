const http = require('http');

const PORT = 8000; // Mocking the backend port

const events = [
  { event_type: "INVESTIGATION_STARTED", data: { investigation_id: "demo-123", objective: "Demo Hackathon Idea" } },
  { event_type: "ROUND_STARTED", data: { round_number: 1, plan: { steps: ["Market Research"] } } },
  { event_type: "RESEARCH_MISSION_CREATED", data: { role: "Market Analyst", query: "Hackathon trends" } },
  { event_type: "RESEARCHER_STARTED", data: { role: "Market Analyst" } },
  { event_type: "CLAIM_CREATED", data: { claim: { id: "c1", statement: "AI tools are popular", verification_status: "UNVERIFIED" } } },
  { event_type: "RESEARCHER_COMPLETED", data: { role: "Market Analyst" } },
  { event_type: "SKEPTIC_STARTED", data: {} },
  { event_type: "CHALLENGE_CREATED", data: { challenge: { target_claim_id: "c1", attack_vector: "Overly broad", counter_argument: "Define AI tools", severity: "HIGH" } } },
  { event_type: "SKEPTIC_COMPLETED", data: {} },
  { event_type: "VERIFIER_STARTED", data: {} },
  { event_type: "VERIFICATION_COMPLETED", data: { claim_index: 0, status: "VERIFIED" } },
  { event_type: "KNOWLEDGE_GAP_IDENTIFIED", data: { gap: { question: "What specific APIs?", priority: "HIGH" } } },
  { event_type: "ROUND_STARTED", data: { round_number: 2, plan: { steps: ["API Research"] } } },
  { event_type: "RESEARCH_MISSION_CREATED", data: { role: "Tech Scout", query: "Top APIs" } },
  { event_type: "RESEARCHER_STARTED", data: { role: "Tech Scout" } },
  { event_type: "RESEARCHER_COMPLETED", data: { role: "Tech Scout" } },
  { event_type: "INVESTIGATION_COMPLETED", data: { verdict: { recommendation: "PROCEED", confidence_score: 95, key_findings: ["AI is good", "Use Gemini"], unresolved_questions: [] } } }
];

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', '*');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.method === 'POST' && req.url === '/api/investigations') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ investigation_id: 'demo-123', status: 'INITIALIZING' }));
    return;
  }

  if (req.method === 'GET' && req.url.startsWith('/api/investigations/') && req.url.endsWith('/stream')) {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    });

    let index = 0;
    const interval = setInterval(() => {
      if (index < events.length) {
        const evt = events[index];
        res.write(`event: ${evt.event_type}\n`);
        res.write(`data: ${JSON.stringify(evt.data)}\n\n`);
        index++;
      } else {
        clearInterval(interval);
        res.end();
      }
    }, 500); // Emit an event every 500ms

    req.on('close', () => clearInterval(interval));
    return;
  }
  
  if (req.method === 'GET' && req.url.startsWith('/api/investigations/')) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      investigation_id: 'demo-123',
      objective: 'Demo Hackathon Idea',
      status: 'COMPLETED',
      current_round: 2,
      rounds: []
    }));
    return;
  }

  res.writeHead(404);
  res.end();
});

server.listen(PORT, () => console.log(`Mock SSE backend listening on port ${PORT}`));
