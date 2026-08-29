"use client";

import React from 'react';
import { InvestigationViewState } from '@/hooks/useInvestigationState';

export default function InvestigationGraph2D({ state }: { state: InvestigationViewState }) {
  const researcherCount = Math.max(state.missions.length, 1);
  
  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8 overflow-hidden font-mono text-xs relative text-white">
      
      {/* Background decoration */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/10 via-black to-black -z-10 pointer-events-none"></div>

      <div className="flex flex-col items-center w-full max-w-2xl relative">
        
        {/* LEAD AGENT */}
        <div className={`p-3 rounded-lg border flex flex-col items-center justify-center z-10 w-48 text-center transition-colors duration-500
          ${state.activeAgents.size === 0 && !state.isComplete ? 'bg-blue-600/30 border-blue-400 text-blue-100 shadow-[0_0_15px_rgba(59,130,246,0.5)]' : 'bg-neutral-900 border-neutral-700 text-neutral-400'}`}>
          <div className="font-bold mb-1">LEAD AGENT</div>
          <div className="text-[10px] opacity-70">Round {state.round} Orchestrator</div>
        </div>

        {/* CONNECTIONS TO RESEARCHERS */}
        <div className="w-px h-8 bg-gradient-to-b from-blue-500/50 to-neutral-700"></div>
        <div className="h-px bg-neutral-700" style={{ width: `${Math.min(researcherCount * 120, 100)}%`, maxWidth: '500px' }}></div>
        <div className="flex w-full justify-around max-w-[500px]">
          {state.missions.length === 0 ? (
             <div className="w-px h-8 bg-neutral-700"></div>
          ) : (
            state.missions.map((_, i) => (
              <div key={i} className="w-px h-8 bg-neutral-700 relative"></div>
            ))
          )}
        </div>

        {/* RESEARCHERS */}
        <div className="flex w-full justify-around max-w-[500px] gap-2">
          {state.missions.length === 0 ? (
            <div className="p-2 rounded border border-dashed border-neutral-700 text-neutral-500 w-32 text-center bg-neutral-900/50">
              Awaiting Missions...
            </div>
          ) : (
            state.missions.map((m, i) => {
              const isActive = m.status === 'running';
              const isCompleted = m.status === 'completed';
              return (
                <div key={i} className={`p-2 rounded border flex flex-col items-center justify-center z-10 flex-1 text-center min-w-[80px] transition-colors duration-500
                  ${isActive ? 'bg-green-600/30 border-green-400 text-green-100 shadow-[0_0_10px_rgba(34,197,94,0.3)]' : 
                    isCompleted ? 'bg-green-900/30 border-green-800 text-green-500' : 'bg-neutral-900 border-neutral-700 text-neutral-400'}`}>
                  <div className="font-bold truncate w-full" title={m.role}>{m.role}</div>
                </div>
              );
            })
          )}
        </div>

        {/* CONNECTIONS TO SKEPTIC */}
        {state.challenges.length > 0 && (
          <>
            <div className="flex w-full justify-around max-w-[500px]">
              {state.missions.map((_, i) => (
                <div key={i} className="w-px h-8 bg-neutral-700"></div>
              ))}
            </div>
            <div className="h-px bg-neutral-700" style={{ width: `${Math.min(researcherCount * 120, 100)}%`, maxWidth: '500px' }}></div>
            <div className="w-px h-8 bg-neutral-700"></div>
            
            {/* SKEPTIC */}
            <div className={`p-3 rounded-lg border flex flex-col items-center justify-center z-10 w-48 text-center transition-colors duration-500
              ${state.activeAgents.has('Skeptic') ? 'bg-orange-600/30 border-orange-400 text-orange-100 shadow-[0_0_15px_rgba(249,115,22,0.4)]' : 'bg-neutral-900 border-neutral-700 text-neutral-400'}`}>
              <div className="font-bold mb-1">SKEPTIC ({state.challenges.length})</div>
              <div className="text-[10px] opacity-70">Adversarial Challenge</div>
            </div>
          </>
        )}

        {/* CONNECTIONS TO VERIFIER */}
        {(state.activeAgents.has('Verifier') || state.verifications.length > 0) && (
          <>
            <div className="w-px h-8 bg-neutral-700"></div>
            {/* VERIFIER */}
            <div className={`p-3 rounded-lg border flex flex-col items-center justify-center z-10 w-48 text-center transition-colors duration-500
              ${state.activeAgents.has('Verifier') ? 'bg-purple-600/30 border-purple-400 text-purple-100 shadow-[0_0_15px_rgba(168,85,247,0.4)]' : 'bg-neutral-900 border-neutral-700 text-neutral-400'}`}>
              <div className="font-bold mb-1">VERIFIER ({state.verifications.length})</div>
              <div className="text-[10px] opacity-70">Independent Fact-Check</div>
            </div>
          </>
        )}

      </div>
    </div>
  );
}
