export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || '';

export interface StartInvestigationRequest {
  objective: string;
  constraints?: string[];
}

export interface StartInvestigationResponse {
  investigation_id: string;
  status: string;
}

export interface Claim {
  id: string;
  statement: string;
  category?: string;
  verification_status: 'UNVERIFIED' | 'VERIFIED' | 'DISPROVED';
  confidence_score?: number;
  sources?: Array<{
    title?: string;
    url?: string;
    snippet?: string;
    source_domain?: string;
    relationship?: 'SUPPORTS' | 'CONTRADICTS' | 'QUALIFIES' | 'IRRELEVANT';
  }>;
}

export interface SkepticChallenge {
  id: string;
  target_claim_id: string;
  attack_vector: string;
  counter_argument: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface VerificationResult {
  claim_id: string;
  verified: boolean;
  notes: string;
  external_sources?: string[];
}

export interface FinalVerdict {
  recommendation: 'PROCEED' | 'PIVOT' | 'ABORT' | string;
  confidence_score: number;
  key_findings: string[];
  tradeoffs?: string[];
  risks?: string[];
  unresolved_questions?: string[];
}

export interface RoundState {
  round_number: number;
  lead_plan?: Record<string, unknown>;
  research_missions?: Record<string, unknown>[];
  claims?: Claim[];
  skeptic_challenges?: SkepticChallenge[];
  verifications?: VerificationResult[];
}

export interface InvestigationState {
  investigation_id: string;
  objective: string;
  constraints: string[];
  status: 'INITIALIZING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  current_round: number;
  rounds: RoundState[];
  final_verdict?: FinalVerdict;
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

export async function getInvestigationStatus(investigationId: string): Promise<InvestigationState> {
  const res = await fetch(`${API_BASE_URL}/api/investigations/${investigationId}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch status: ${res.statusText}`);
  }
  return res.json();
}

export async function getVerdict(investigationId: string): Promise<FinalVerdict> {
  const res = await fetch(`${API_BASE_URL}/api/investigations/${investigationId}/verdict`);
  if (!res.ok) {
    throw new Error(`Failed to fetch verdict: ${res.statusText}`);
  }
  return res.json();
}
