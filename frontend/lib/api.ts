export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export interface StartInvestigationRequest {
  objective: string;
  constraints?: string[];
}

export interface StartInvestigationResponse {
  investigation_id: string;
  status: string;
}

export async function startInvestigation(req: StartInvestigationRequest): Promise<StartInvestigationResponse> {
  const res = await fetch(`${API_BASE_URL}/api/investigations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error(`Failed to start investigation: ${res.statusText}`);
  }
  return res.json();
}

export async function getVerdict(investigationId: string): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/investigations/${investigationId}/verdict`);
  if (!res.ok) {
    throw new Error(`Failed to fetch verdict: ${res.statusText}`);
  }
  return res.json();
}
