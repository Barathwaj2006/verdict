"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import { getInvestigationStatus, getVerdict, InvestigationState, FinalVerdict } from '../../../lib/api';
import { useInvestigationSSE } from '../../../hooks/useInvestigationSSE';
import TelemetryStream from '../../../components/TelemetryStream';
import AgentGraph from '../../../components/AgentGraph';
import EvidenceMatrix from '../../../components/EvidenceMatrix';
import FinalVerdictReport from '../../../components/FinalVerdictReport';

export default function WorkspacePage() {
  const params = useParams();
  const router = useRouter();
  const investigationId = params?.id as string;

  const [state, setState] = useState<InvestigationState | null>(null);
  const [verdict, setVerdict] = useState<FinalVerdict | null>(null);
  const [selectedRound, setSelectedRound] = useState<number>(1);

  const { events, isConnected } = useInvestigationSSE(investigationId);

  const fetchStatus = useCallback(async () => {
    if (!investigationId) return;
    try {
      const data = await getInvestigationStatus(investigationId);
      setState(data);
      if (data.current_round) {
        setSelectedRound(data.current_round);
      }
      if (data.status === 'COMPLETED' || data.final_verdict) {
        const vData = data.final_verdict || (await getVerdict(investigationId));
        setVerdict(vData);
      }
    } catch (err: unknown) {
      console.error('Failed to fetch investigation status:', err);
    }
  }, [investigationId]);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  const currentRoundObj = state?.rounds?.find((r) => r.round_number === selectedRound) || state?.rounds?.[0];
  const claims = currentRoundObj?.claims || [];
  const challenges = currentRoundObj?.skeptic_challenges || [];

  return (
    <div className="min-h-screen bg-[#07080C] text-gray-100 flex flex-col justify-between relative overflow-hidden">
      {/* Background Ambience */}
      <div className="absolute top-0 left-1/3 w-[500px] h-[300px] bg-indigo-600/10 rounded-full blur-[140px] pointer-events-none" />

      {/* Header */}
      <header className="px-6 py-4 border-b border-white/10 glass-panel flex items-center justify-between z-10 sticky top-0">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push('/')}
            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white transition-all border border-white/10"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-sm tracking-wide text-white font-mono">
                INVESTIGATION #{investigationId?.slice(0, 8)}
              </h1>
              <span className="px-2 py-0.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-[10px] font-mono">
                {state?.status || 'RUNNING'}
              </span>
            </div>
            <p className="text-[11px] text-gray-400 font-sans line-clamp-1 max-w-md">
              {state?.objective || 'Loading objective...'}
            </p>
          </div>
        </div>

        {/* Round Switcher & Actions */}
        <div className="flex items-center gap-3">
          {state?.rounds && state.rounds.length > 0 && (
            <div className="flex items-center gap-1 bg-[#0D0F17] p-1 rounded-xl border border-white/10">
              {state.rounds.map((r) => (
                <button
                  key={r.round_number}
                  onClick={() => setSelectedRound(r.round_number)}
                  className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-all ${
                    selectedRound === r.round_number
                      ? 'bg-indigo-600 text-white shadow-md'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Round {r.round_number}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={fetchStatus}
            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white transition-all border border-white/10"
            title="Refresh Status"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Main Grid Workspace */}
      <main className="max-w-7xl mx-auto px-6 py-6 flex-1 w-full space-y-6 z-10">
        {/* Final Verdict Banner (If Completed) */}
        {(verdict || state?.final_verdict) && (
          <FinalVerdictReport
            verdict={verdict || state!.final_verdict!}
            objective={state?.objective || ''}
          />
        )}

        {/* Workspace Telemetry & Agent Graph Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[520px]">
          {/* Left Column: Real-time Telemetry Stream */}
          <div className="lg:col-span-4 h-full">
            <TelemetryStream
              events={events}
              isConnected={isConnected}
            />
          </div>

          {/* Right Column: Dynamic Agent Graph */}
          <div className="lg:col-span-8 h-full">
            <AgentGraph state={state} selectedRound={selectedRound} />
          </div>
        </div>

        {/* Bottom Section: Evidence Matrix & Claims */}
        <EvidenceMatrix claims={claims} challenges={challenges} />
      </main>

      {/* Footer */}
      <footer className="px-6 py-3 border-t border-white/5 text-center text-xs text-gray-500 font-mono glass-panel">
        VERDICT Command Center &bull; Round-by-Round Firestore Persisted &bull; Grounded Evidence Matrix
      </footer>
    </div>
  );
}
