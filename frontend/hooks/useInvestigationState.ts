"use client";

import { useMemo } from "react";
import { useInvestigationSSE, SSEEvent } from "./useInvestigationSSE";
import { Claim, SkepticChallenge, FinalVerdict } from "@/lib/api";

export interface AgentMission {
  role: string;
  query: string;
  status: "pending" | "running" | "completed" | "failed";
}

export interface Verification {
  claim_index?: number;
  status?: string;
  claim_id?: string;
  verified?: boolean;
  notes?: string;
  external_sources?: string[];
}

export interface InvestigationViewState {
  investigationId: string | null;
  events: SSEEvent[];
  isConnected: boolean;
  isComplete: boolean;
  objective: string;
  round: number;
  missions: AgentMission[];
  claims: Claim[];
  challenges: SkepticChallenge[];
  verifications: Verification[];
  knowledgeGaps: Array<{ question?: string; priority?: string } | Record<string, unknown>>;
  finalVerdict: FinalVerdict | null;
  activeAgents: Set<string>;
}

export function useInvestigationState(investigationId: string | null): InvestigationViewState {
  const { events: rawEvents, isConnected } = useInvestigationSSE(investigationId);
  
  // Deduplicate events to prevent React strict mode double-renders
  const events = useMemo(() => {
    const seen = new Set<string>();
    return rawEvents.filter(e => {
      const key = `${e.timestamp}-${e.event_type}-${JSON.stringify(e.data).length}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }, [rawEvents]);

  const state = useMemo(() => {
    const s: InvestigationViewState = {
      investigationId,
      events,
      isConnected,
      isComplete: false,
      objective: "",
      round: 1,
      missions: [],
      claims: [],
      challenges: [],
      verifications: [],
      knowledgeGaps: [],
      finalVerdict: null,
      activeAgents: new Set(),
    };

    events.forEach(e => {
      const d = (e.data || {}) as Record<string, unknown>;
      
      if (e.event_type === "INVESTIGATION_STARTED") {
        s.objective = (d.objective as string) || s.objective;
      }
      if (e.event_type === "ROUND_STARTED") {
        s.round = (d.round_number as number) || s.round;
      }
      if (e.event_type === "RESEARCH_MISSION_CREATED") {
        s.missions.push({ role: (d.role as string) || '', query: (d.query as string) || '', status: "pending" });
      }
      if (e.event_type === "RESEARCHER_STARTED") {
        const role = (d.role as string) || "Researcher";
        s.activeAgents.add(role);
        const m = s.missions.find(m => m.role === role);
        if (m) m.status = "running";
      }
      if (e.event_type === "RESEARCHER_COMPLETED") {
        const role = (d.role as string) || "Researcher";
        s.activeAgents.delete(role);
        const m = s.missions.find(m => m.role === role);
        if (m) m.status = "completed";
      }
      if (e.event_type === "CLAIM_CREATED" && d.claim) {
        s.claims.push(d.claim as Claim);
      }
      if (e.event_type === "CHALLENGE_CREATED" && d.challenge) {
        s.challenges.push(d.challenge as SkepticChallenge);
      }
      if (e.event_type === "SKEPTIC_STARTED") {
        s.activeAgents.add("Skeptic");
      }
      if (e.event_type === "SKEPTIC_COMPLETED") {
        s.activeAgents.delete("Skeptic");
      }
      if (e.event_type === "VERIFIER_STARTED") {
        s.activeAgents.add("Verifier");
      }
      if (e.event_type === "VERIFICATION_COMPLETED") {
        s.activeAgents.delete("Verifier");
        s.verifications.push((d.verification || d) as Verification);
        const idx = d.claim_index as number | undefined;
        if (idx !== undefined && s.claims[idx]) {
          s.claims[idx].verification_status = ((d.status as 'UNVERIFIED' | 'VERIFIED' | 'DISPROVED') || s.claims[idx].verification_status);
        }
      }
      if (e.event_type === "KNOWLEDGE_GAP_IDENTIFIED" && d.gap) {
        s.knowledgeGaps.push(d.gap as { question?: string; priority?: string });
      }
      if (e.event_type === "INVESTIGATION_COMPLETED") {
        s.isComplete = true;
        s.finalVerdict = (d.verdict as FinalVerdict) || null;
      }
    });

    return s;
  }, [events, investigationId, isConnected]);

  return state;
}
