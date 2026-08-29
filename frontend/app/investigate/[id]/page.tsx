"use client";

import { useInvestigationStream } from '@/hooks/useInvestigationStream';
import { useEffect, useState } from 'react';
import { getVerdict } from '@/lib/api';

export default function InvestigatePage({ params }: { params: { id: string } }) {
  const { events, status } = useInvestigationStream(params.id);
  const [verdict, setVerdict] = useState<any>(null);

  useEffect(() => {
    if (status === 'COMPLETED') {
      getVerdict(params.id).then(setVerdict).catch(console.error);
    }
  }, [status, params.id]);

  const leadEvents = events.filter(e => e.agent === 'LEAD');
  const skepticEvents = events.filter(e => e.agent === 'SKEPTIC');
  const verifierEvents = events.filter(e => e.agent === 'VERIFIER');
  
  // Aggregate missions
  const missions = events.filter(e => e.event_type === 'RESEARCH_MISSION_CREATED').map(e => e.payload);
  const researchersActive = events.some(e => e.event_type === 'RESEARCHER_STARTED' && e.round_number === Math.max(...events.map(ev => ev.round_number || 1)));
  
  const currentRound = Math.max(1, ...events.map(e => e.round_number || 1));

  return (
    <main className="min-h-screen bg-neutral-950 text-neutral-200 flex flex-col md:flex-row font-sans">
      
      {/* LEFT PANEL: TIMELINE & META */}
      <section className="w-full md:w-1/3 border-r border-neutral-800 p-6 flex flex-col overflow-y-auto">
        <div className="mb-6">
          <h2 className="text-xl font-bold mb-2 tracking-tight">VERDICT Investigation</h2>
          <div className="text-sm font-mono text-neutral-500 mb-2">ID: {params.id}</div>
          <div className="flex items-center gap-2">
            <span className={`h-2 w-2 rounded-full ${status === 'CONNECTED' ? 'bg-green-500' : status === 'COMPLETED' ? 'bg-blue-500' : status === 'FAILED' ? 'bg-red-500' : 'bg-yellow-500 animate-pulse'}`}></span>
            <span className="text-sm font-semibold">{status} (Round {currentRound})</span>
          </div>
        </div>

        <div className="flex-1">
          <h3 className="text-xs uppercase tracking-wider text-neutral-500 font-bold mb-4">Live Activity</h3>
          <div className="space-y-4">
            {events.map((e, idx) => (
              <div key={e._id || idx} className="text-sm">
                <div className="text-neutral-500 font-mono text-xs">{new Date(e.timestamp).toLocaleTimeString()}</div>
                <div className={`mt-1 font-medium ${e.agent === 'SKEPTIC' ? 'text-orange-400' : e.agent === 'VERIFIER' ? 'text-purple-400' : e.agent === 'LEAD' ? 'text-blue-400' : 'text-green-400'}`}>
                  {e.event_type.replace(/_/g, ' ')}
                </div>
                {e.payload?.claim?.content && <div className="text-neutral-400 text-xs mt-1 italic">"{e.payload.claim.content}"</div>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CENTER PANEL: AGENT GRAPH & RECURSION */}
      <section className="w-full md:w-1/3 border-r border-neutral-800 p-6 flex flex-col bg-neutral-900 overflow-y-auto">
        <h3 className="text-xs uppercase tracking-wider text-neutral-500 font-bold mb-6">Agent Visualization</h3>
        
        <div className="flex flex-col items-center space-y-6">
          {/* LEAD */}
          <div className={`p-4 rounded-xl border ${leadEvents.length ? 'border-blue-500 bg-blue-500/10' : 'border-neutral-700 bg-neutral-800'} w-64 text-center`}>
            <div className="font-bold text-blue-400">LEAD AGENT</div>
            <div className="text-xs text-neutral-400 mt-1">Orchestrator</div>
          </div>
          
          <div className="h-6 border-l border-dashed border-neutral-700"></div>
          
          {/* RESEARCHERS */}
          <div className="grid grid-cols-2 gap-4 w-full">
            {missions.length === 0 ? (
              <div className="col-span-2 text-center text-sm text-neutral-500 py-4 border border-neutral-800 rounded-xl bg-neutral-900">
                Awaiting research missions...
              </div>
            ) : (
              missions.map((m, i) => (
                <div key={i} className={`p-4 rounded-xl border ${researchersActive ? 'border-green-500 bg-green-500/10' : 'border-neutral-700 bg-neutral-800'} text-center flex flex-col items-center justify-center`}>
                  <div className="font-bold text-green-400 text-sm leading-tight">{m.role || 'Specialist'}</div>
                </div>
              ))
            )}
          </div>
          
          <div className="h-6 border-l border-dashed border-neutral-700"></div>

          {/* SKEPTIC */}
          <div className={`p-4 rounded-xl border ${skepticEvents.length ? 'border-orange-500 bg-orange-500/10' : 'border-neutral-700 bg-neutral-800'} w-64 text-center`}>
            <div className="font-bold text-orange-400">SKEPTIC AGENT</div>
            <div className="text-xs text-neutral-400 mt-1">Challenger</div>
          </div>
          
          <div className="h-6 border-l border-dashed border-neutral-700"></div>

          {/* VERIFIER */}
          <div className={`p-4 rounded-xl border ${verifierEvents.length ? 'border-purple-500 bg-purple-500/10' : 'border-neutral-700 bg-neutral-800'} w-64 text-center`}>
            <div className="font-bold text-purple-400">VERIFIER AGENT</div>
            <div className="text-xs text-neutral-400 mt-1">Adjudicator</div>
          </div>
          
          {events.some(e => e.event_type === 'LEAD_DECISION') && (
            <>
              <div className="h-6 border-l border-dashed border-neutral-700"></div>
              <div className={`p-4 rounded-xl border border-yellow-500 bg-yellow-500/10 w-64 text-center`}>
                <div className="font-bold text-yellow-400">EVALUATION</div>
                <div className="text-xs text-neutral-300 mt-1">
                  {events.filter(e => e.event_type === 'LEAD_DECISION').pop()?.payload?.decision || 'Deciding...'}
                </div>
              </div>
            </>
          )}
        </div>
      </section>

      {/* RIGHT PANEL: VERDICT & EVIDENCE */}
      <section className="w-full md:w-1/3 p-6 bg-neutral-950 overflow-y-auto">
        <h3 className="text-xs uppercase tracking-wider text-neutral-500 font-bold mb-4">Findings & Verdict</h3>
        
        {verdict ? (
          <div className="p-6 bg-blue-900/20 border border-blue-800 rounded-xl mb-6">
            <h2 className="text-2xl font-bold text-white mb-4">FINAL VERDICT</h2>
            <div className="text-neutral-200 mb-4 whitespace-pre-wrap">{verdict.conclusion}</div>
            
            <div className="grid grid-cols-2 gap-4 mt-6">
              <div className="bg-black/20 p-3 rounded-lg border border-white/5">
                <div className="text-xs text-neutral-400 mb-1">Confidence</div>
                <div className="font-semibold text-lg">{verdict.confidence}/10</div>
              </div>
              <div className="bg-black/20 p-3 rounded-lg border border-white/5">
                <div className="text-xs text-neutral-400 mb-1">Verified Claims</div>
                <div className="font-semibold text-lg">{verdict.verified_claims?.length || 0}</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center p-8 border border-dashed border-neutral-800 rounded-xl text-neutral-600 mb-6">
            Investigation in progress... <br/> Final verdict will appear here.
          </div>
        )}

        <div className="space-y-4">
          <h4 className="font-semibold text-neutral-400 border-b border-neutral-800 pb-2">Claims Pipeline</h4>
          {events.filter(e => e.event_type === 'CLAIM_CREATED').map((e, idx) => (
            <div key={idx} className="p-4 bg-neutral-900 border border-neutral-800 rounded-lg text-sm">
              <div className="font-medium text-neutral-300 mb-2">{e.payload.claim?.content}</div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-neutral-500">Source: <a href={e.payload.claim?.source_url} target="_blank" rel="noreferrer" className="text-blue-400 hover:underline">Link</a></span>
                <span className="px-2 py-1 rounded bg-neutral-800 font-mono text-neutral-400">{e.payload.claim?.status || 'UNVERIFIED'}</span>
              </div>
            </div>
          ))}
        </div>
      </section>
      
    </main>
  );
}
