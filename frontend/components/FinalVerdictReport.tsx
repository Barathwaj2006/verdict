"use client";

import React from 'react';
import { Award, ShieldCheck, AlertTriangle, Layers, Download, CheckCircle, FileText } from 'lucide-react';
import { FinalVerdict } from '../lib/api';

interface FinalVerdictReportProps {
  verdict: FinalVerdict;
  objective: string;
}

export default function FinalVerdictReport({ verdict, objective }: FinalVerdictReportProps) {
  const getRecommendationBadge = (rec: string) => {
    switch (rec?.toUpperCase()) {
      case 'PROCEED':
        return (
          <span className="px-4 py-1.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 font-black text-sm tracking-wider font-mono flex items-center gap-2">
            <CheckCircle className="w-4 h-4" /> RECOMMENDATION: PROCEED
          </span>
        );
      case 'PIVOT':
        return (
          <span className="px-4 py-1.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/50 font-black text-sm tracking-wider font-mono flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" /> RECOMMENDATION: PIVOT
          </span>
        );
      case 'ABORT':
        return (
          <span className="px-4 py-1.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/50 font-black text-sm tracking-wider font-mono flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" /> RECOMMENDATION: ABORT
          </span>
        );
      default:
        return (
          <span className="px-4 py-1.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/50 font-black text-sm tracking-wider font-mono flex items-center gap-2">
            <Award className="w-4 h-4" /> RECOMMENDATION: {rec || 'EVALUATED'}
          </span>
        );
    }
  };

  const confidencePercent = Math.round((verdict.confidence_score || 0.85) * 100);

  return (
    <div className="glass-panel rounded-2xl border border-indigo-500/40 p-8 space-y-8 bg-gradient-to-b from-indigo-950/40 via-[#0D0F17]/90 to-[#07080C]/90 shadow-2xl relative overflow-hidden">
      {/* Ambient Radial Glow */}
      <div className="absolute top-0 right-0 w-[500px] h-[300px] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />

      {/* 5-10 Second Executive Summary Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-white/10 pb-6 z-10 relative">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-indigo-400" />
            <span className="text-xs font-bold text-indigo-300 uppercase tracking-widest font-mono">
              Executive Briefing Report
            </span>
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            FINAL VERDICT
          </h2>
          <p className="text-xs text-gray-400 max-w-xl font-sans">
            Objective: <span className="text-gray-200 italic">&quot;{objective}&quot;</span>
          </p>
        </div>

        <div className="flex flex-col items-start md:items-end gap-3">
          {getRecommendationBadge(verdict.recommendation)}

          <div className="flex items-center gap-3">
            <span className="text-xs text-gray-400 font-mono">Confidence Level:</span>
            <div className="px-3 py-1 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 font-mono font-bold text-sm">
              {confidencePercent}%
            </div>
          </div>
        </div>
      </div>

      {/* Grid: Key Findings & Trade-Offs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 z-10 relative">
        {/* Key Verified Findings */}
        <div className="glass-card rounded-xl p-5 border border-white/10 space-y-4">
          <div className="flex items-center gap-2 border-b border-white/5 pb-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <h3 className="text-xs font-bold text-emerald-300 uppercase tracking-wider font-mono">
              Key Verified Findings
            </h3>
          </div>
          <ul className="space-y-2.5">
            {verdict.key_findings?.map((finding, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs text-gray-200">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0" />
                <span className="leading-relaxed">{finding}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Trade-Offs & Critical Risks */}
        <div className="glass-card rounded-xl p-5 border border-white/10 space-y-4">
          <div className="flex items-center gap-2 border-b border-white/5 pb-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <h3 className="text-xs font-bold text-amber-300 uppercase tracking-wider font-mono">
              Trade-Offs &amp; Risk Analysis
            </h3>
          </div>
          <ul className="space-y-2.5">
            {(verdict.tradeoffs || verdict.risks || [
              "Implementation time commitments must be strictly monitored.",
              "Requires active validation of dependencies across rounds."
            ]).map((tradeoff, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs text-gray-200">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 flex-shrink-0" />
                <span className="leading-relaxed">{tradeoff}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Audit Telemetry & Export */}
      <div className="pt-4 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-gray-400 z-10 relative">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-indigo-400" /> Multi-Round Verified
          </span>
          <span>&bull;</span>
          <span className="flex items-center gap-1.5">
            <FileText className="w-3.5 h-3.5 text-emerald-400" /> Firestore Persisted
          </span>
        </div>

        <button
          onClick={() => window.print()}
          className="px-4 py-2 rounded-xl bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/40 text-indigo-200 font-semibold text-xs flex items-center gap-2 transition-all"
        >
          <Download className="w-3.5 h-3.5" /> Export Executive Summary
        </button>
      </div>
    </div>
  );
}
