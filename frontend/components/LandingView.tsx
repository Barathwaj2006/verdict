"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Sparkles, ArrowRight, ShieldCheck, Cpu, GitBranch, Layers } from 'lucide-react';
import { startInvestigation } from '../lib/api';

const EXAMPLE_PROMPTS = [
  "Find me the strongest project idea for this hackathon. I have 3 days and I am working alone using Google GenAI APIs.",
  "Determine whether our team should migrate from Node.js to Python / FastAPI for ML workloads.",
  "Evaluate building an autonomous AI code review bot vs. an AI customer support platform.",
];

export default function LandingView() {
  const router = useRouter();
  const [objective, setObjective] = useState('');
  const [constraintsText, setConstraintsText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!objective.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const constraints = constraintsText
        .split('\n')
        .map((c) => c.trim())
        .filter(Boolean);

      const res = await startInvestigation({ objective, constraints });
      router.push(`/workspace/${res.investigation_id}`);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to initiate investigation.';
      setError(msg);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#07080C] text-gray-100 flex flex-col justify-between relative overflow-hidden">
      {/* Subtle Background Glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-indigo-600/10 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-[400px] h-[300px] bg-emerald-600/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Header */}
      <header className="px-8 py-6 flex items-center justify-between border-b border-white/10 glass-panel z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-[#818CF8] text-indigo-400 font-black text-lg shadow-sm shadow-indigo-500/20">
            <span className="mx-auto">V</span>
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-wider text-white">VERDICT</h1>
            <p className="text-[10px] text-gray-400 uppercase tracking-widest font-mono">Autonomous Decision Engine</p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs">
          <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5 font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            Gemini 2.5 Flash Engine
          </span>
          <span className="px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 font-mono">
            Phase 1 Frozen (35 Tests Passed)
          </span>
        </div>
      </header>

      {/* Main Hero & Input */}
      <main className="max-w-4xl mx-auto px-6 py-12 flex-1 flex flex-col justify-center z-10 w-full">
        <div className="text-center mb-8 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-mono mb-2">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            Adversarial Multi-Agent Research Engine
          </div>
          <h2 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            High-Stakes Decision Research <br />
            <span className="bg-gradient-to-r from-indigo-400 via-sky-400 to-emerald-400 bg-clip-text text-transparent">
              Backed by Grounded Evidence
            </span>
          </h2>
          <p className="text-gray-400 text-sm sm:text-base max-w-2xl mx-auto">
            State your decision objective. VERDICT deploys dynamic specialist researchers, attacks claims with a Skeptic Agent, verifies sources independently, and recursively closes knowledge gaps.
          </p>
        </div>

        {/* Form Input Container */}
        <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-2xl border border-white/10 shadow-2xl space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-gray-300 uppercase tracking-wider font-mono flex items-center justify-between">
              <span>Decision Objective</span>
              <span className="text-gray-500 text-[11px] font-sans">Natural Language Input</span>
            </label>
            <textarea
              rows={3}
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              placeholder="e.g. Should we adopt Rust microservices for our core billing backend?"
              className="w-full bg-[#0D0F17]/90 border border-white/15 rounded-xl p-4 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-sm resize-none transition-all"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-gray-300 uppercase tracking-wider font-mono">
              Constraints &amp; Context (Optional)
            </label>
            <textarea
              rows={2}
              value={constraintsText}
              onChange={(e) => setConstraintsText(e.target.value)}
              placeholder="Enter optional constraints (one per line, e.g. Team size: 3 developers)"
              className="w-full bg-[#0D0F17]/90 border border-white/15 rounded-xl p-3 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-xs resize-none transition-all font-mono"
            />
          </div>

          {error && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !objective.trim()}
            className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-indigo-600 via-sky-600 to-indigo-600 hover:from-indigo-500 hover:to-sky-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Initializing Multi-Agent Telemetry...</span>
              </>
            ) : (
              <>
                <span>Initiate Autonomous Investigation</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        {/* Prompt Suggestions */}
        <div className="mt-6 space-y-2">
          <p className="text-xs text-gray-500 font-mono text-center">Or try an example investigation prompt:</p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {EXAMPLE_PROMPTS.map((prompt, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setObjective(prompt)}
                className="p-3 text-left rounded-xl glass-card hover:border-indigo-500/40 text-xs text-gray-400 hover:text-gray-200 transition-all border border-white/5 line-clamp-3"
              >
                &quot;{prompt}&quot;
              </button>
            ))}
          </div>
        </div>

        {/* Feature Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-12">
          <div className="p-4 rounded-xl glass-card border border-white/5 text-center space-y-1">
            <Cpu className="w-5 h-5 text-indigo-400 mx-auto" />
            <div className="text-xs font-bold text-gray-200">Dynamic Lead</div>
            <div className="text-[11px] text-gray-500">Gemini 2.5 Briefing</div>
          </div>
          <div className="p-4 rounded-xl glass-card border border-white/5 text-center space-y-1">
            <GitBranch className="w-5 h-5 text-sky-400 mx-auto" />
            <div className="text-xs font-bold text-gray-200">Adversarial Skeptic</div>
            <div className="text-[11px] text-gray-500">Counter-Evidence Attack</div>
          </div>
          <div className="p-4 rounded-xl glass-card border border-white/5 text-center space-y-1">
            <ShieldCheck className="w-5 h-5 text-emerald-400 mx-auto" />
            <div className="text-xs font-bold text-gray-200">Verifier Audit</div>
            <div className="text-[11px] text-gray-500">Ground Truth Check</div>
          </div>
          <div className="p-4 rounded-xl glass-card border border-white/5 text-center space-y-1">
            <Layers className="w-5 h-5 text-amber-400 mx-auto" />
            <div className="text-xs font-bold text-gray-200">Recursive Loop</div>
            <div className="text-[11px] text-gray-500">Gap Closure Rounds</div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="px-8 py-4 border-t border-white/5 text-center text-xs text-gray-500 font-mono glass-panel">
        VERDICT Autonomous Decision Engine &bull; Google Cloud Run &amp; Firestore Ready &bull; MIT License
      </footer>
    </div>
  );
}
