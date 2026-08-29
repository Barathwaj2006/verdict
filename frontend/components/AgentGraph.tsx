"use client";

import React from 'react';
import { Cpu, Search, AlertTriangle, ShieldCheck, GitBranch } from 'lucide-react';
import { InvestigationState } from '../lib/api';

interface AgentGraphProps {
  state: InvestigationState | null;
  selectedRound: number;
}

interface MissionItem {
  title?: string;
  researcher_role?: string;
  objective?: string;
  role?: string;
}

export default function AgentGraph({ state, selectedRound }: AgentGraphProps) {
  const currentRoundState = state?.rounds?.find((r) => r.round_number === selectedRound) || state?.rounds?.[0];
  const missions: MissionItem[] = (currentRoundState?.research_missions as MissionItem[]) || [
    { title: "Landscape Specialist", role: "Competitor & Market Context" },
    { title: "Feasibility Specialist", role: "Technical Stack & Risk Analysis" },
    { title: "Opportunity Specialist", role: "Differentiation & User Impact" },
  ];

  return (
    <div className="h-full glass-panel rounded-2xl border border-white/10 p-6 flex flex-col justify-between relative overflow-hidden bg-gradient-to-b from-[#0D0F17]/90 to-[#07080C]/90">
      {/* Background Grid Pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none" />

      {/* Header Info */}
      <div className="flex items-center justify-between z-10 mb-4">
        <div className="flex items-center gap-2">
          <GitBranch className="w-4 h-4 text-indigo-400" />
          <h3 className="text-xs font-bold text-gray-200 uppercase tracking-wider font-mono">
            Dynamic Multi-Agent Hierarchy (Round {selectedRound})
          </h3>
        </div>
        <span className="text-[10px] text-gray-400 font-mono bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded-full">
          {missions.length} Active Missions
        </span>
      </div>

      {/* Agent Graph Tree Container */}
      <div className="flex-1 flex flex-col items-center justify-center gap-6 z-10 py-2">
        {/* Tier 1: Lead Agent Node */}
        <div className="flex flex-col items-center">
          <div className="px-5 py-3 rounded-xl bg-indigo-950/80 border border-indigo-500/50 shadow-lg shadow-indigo-500/20 text-center space-y-1 w-64 backdrop-blur-md">
            <div className="flex items-center justify-center gap-2 text-indigo-300 font-bold text-xs">
              <Cpu className="w-4 h-4 text-indigo-400" />
              Lead Agent (Orchestrator)
            </div>
            <p className="text-[10px] text-indigo-200/70 font-mono">Gemini 2.5 Flash Briefing</p>
          </div>
          {/* Connector Line */}
          <div className="w-0.5 h-6 bg-indigo-500/40" />
        </div>

        {/* Tier 2: Dynamic Specialist Researchers */}
        <div className="w-full flex justify-center items-center gap-4 flex-wrap">
          {missions.map((mission: MissionItem, idx: number) => (
            <div
              key={idx}
              className="px-4 py-2.5 rounded-xl bg-sky-950/70 border border-sky-500/40 shadow-md text-center space-y-0.5 min-w-[170px] flex-1 max-w-[220px] backdrop-blur-md"
            >
              <div className="flex items-center justify-center gap-1.5 text-sky-300 font-semibold text-xs">
                <Search className="w-3.5 h-3.5 text-sky-400" />
                {mission.title || mission.researcher_role || `Researcher ${idx + 1}`}
              </div>
              <p className="text-[10px] text-sky-200/60 font-mono truncate">
                {mission.objective || mission.role || "Web Evidence Acquisition"}
              </p>
            </div>
          ))}
        </div>

        {/* Connector Lines to Adversarial Layer */}
        <div className="w-0.5 h-6 bg-white/20" />

        {/* Tier 3: Skeptic & Verifier Layer */}
        <div className="flex items-center gap-4">
          <div className="px-4 py-2.5 rounded-xl bg-rose-950/70 border border-rose-500/40 shadow-md text-center space-y-0.5 w-48 backdrop-blur-md">
            <div className="flex items-center justify-center gap-1.5 text-rose-300 font-semibold text-xs">
              <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
              Skeptic Agent
            </div>
            <p className="text-[10px] text-rose-200/60 font-mono">Counter-Evidence Attack</p>
          </div>

          <div className="w-4 h-0.5 bg-white/20" />

          <div className="px-4 py-2.5 rounded-xl bg-emerald-950/70 border border-emerald-500/40 shadow-md text-center space-y-0.5 w-48 backdrop-blur-md">
            <div className="flex items-center justify-center gap-1.5 text-emerald-300 font-semibold text-xs">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              Verifier Agent
            </div>
            <p className="text-[10px] text-emerald-200/60 font-mono">Ground Truth Audit</p>
          </div>
        </div>
      </div>

      {/* Footer / Legend */}
      <div className="pt-3 border-t border-white/5 flex items-center justify-between text-[10px] text-gray-500 font-mono z-10">
        <span>Round {selectedRound} Execution Hierarchy</span>
        <span>Concurrent DuckDuckGo Engine &bull; Non-CoT Payload</span>
      </div>
    </div>
  );
}
