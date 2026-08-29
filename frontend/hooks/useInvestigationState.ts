"use client";

import { useMemo, useState, useEffect, useRef } from "react";
import { useInvestigationSSE, SSEEvent } from "./useInvestigationSSE";

import { Claim, SkepticChallenge } from "@/lib/api";

export interface AgentMission {
  role: string;
  query: string;
  status: "pending" | "running" | "completed" | "failed";
}

export interface Verification {
  claim_index: number;
  status: string;
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
  knowledgeGaps: any[];
  finalVerdict: any | null;
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
      const d = e.data || {};
      
      if (e.event_type === "INVESTIGATION_STARTED") {
        s.objective = d.objective || s.objective;
      }
      if (e.event_type === "ROUND_STARTED") {
        s.round = d.round_number || s.round;
      }
      if (e.event_type === "RESEARCH_MISSION_CREATED") {
        s.missions.push({ role: d.role, query: d.query, status: "pending" });
      }
      if (e.event_type === "RESEARCHER_STARTED") {
        s.activeAgents.add(d.role || "Researcher");
        const m = s.missions.find(m => m.role === d.role);
        if (m) m.status = "running";
      }
      if (e.event_type === "RESEARCHER_COMPLETED") {
        s.activeAgents.delete(d.role || "Researcher");
        const m = s.missions.find(m => m.role === d.role);
        if (m) m.status = "completed";
      }
      if (e.event_type === "CLAIM_CREATED") {
        s.claims.push(d.claim);
      }
      if (e.event_type === "CHALLENGE_CREATED") {
        s.challenges.push(d.challenge);
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
        s.verifications.push(d.verification || d);
        if (d.claim_index !== undefined && s.claims[d.claim_index]) {
            s.claims[d.claim_index].verification_status = d.status || s.claims[d.claim_index].verification_status;
        }
      }
      if (e.event_type === "KNOWLEDGE_GAP_IDENTIFIED") {
        s.knowledgeGaps.push(d.gap);
      }
      if (e.event_type === "INVESTIGATION_COMPLETED") {
        s.isComplete = true;
        s.finalVerdict = d.verdict;
      }
    });

    return s;
  }, [events, investigationId, isConnected]);

  return state;
}
