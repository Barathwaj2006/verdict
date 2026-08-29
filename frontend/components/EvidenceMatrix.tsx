"use client";

import React from 'react';
import { ShieldCheck, AlertTriangle, HelpCircle, ExternalLink, Link2 } from 'lucide-react';
import { Claim, SkepticChallenge } from '../lib/api';

interface EvidenceMatrixProps {
  claims: Claim[];
  challenges: SkepticChallenge[];
  onSelectClaim?: (claim: Claim) => void;
}

export default function EvidenceMatrix({ claims, challenges, onSelectClaim }: EvidenceMatrixProps) {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'VERIFIED':
        return (
          <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono flex items-center gap-1">
            <ShieldCheck className="w-3 h-3" /> VERIFIED
          </span>
        );
      case 'DISPROVED':
        return (
          <span className="px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/30 text-[10px] font-mono flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" /> DISPROVED
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full bg-gray-500/10 text-gray-400 border border-gray-500/30 text-[10px] font-mono flex items-center gap-1">
            <HelpCircle className="w-3 h-3" /> UNVERIFIED
          </span>
        );
    }
  };

  const getRelationshipBadge = (rel?: string) => {
    switch (rel) {
      case 'SUPPORTS':
        return <span className="text-emerald-400 font-mono text-[10px]">[SUPPORTS]</span>;
      case 'CONTRADICTS':
        return <span className="text-rose-400 font-mono text-[10px]">[CONTRADICTS]</span>;
      case 'QUALIFIES':
        return <span className="text-amber-400 font-mono text-[10px]">[QUALIFIES]</span>;
      default:
        return <span className="text-gray-500 font-mono text-[10px]">[CITATION]</span>;
    }
  };

  return (
    <div className="glass-panel rounded-2xl border border-white/10 p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-white/10 pb-3">
        <div className="flex items-center gap-2">
          <Link2 className="w-4 h-4 text-sky-400" />
          <h3 className="text-xs font-bold text-gray-200 uppercase tracking-wider font-mono">
            Evidence Matrix &amp; Claims Audit ({claims.length})
          </h3>
        </div>
      </div>

      {claims.length === 0 ? (
        <p className="text-xs text-gray-500 py-6 text-center font-mono">
          No structured claims recorded for this round yet.
        </p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {claims.map((claim) => {
            const challenge = challenges.find((c) => c.target_claim_id === claim.id);
            return (
              <div
                key={claim.id}
                onClick={() => onSelectClaim && onSelectClaim(claim)}
                className="p-4 rounded-xl glass-card border border-white/5 hover:border-indigo-500/30 cursor-pointer transition-all space-y-3 flex flex-col justify-between"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-[10px] text-gray-500 font-mono">ID: {claim.id}</span>
                    {getStatusBadge(claim.verification_status)}
                  </div>

                  <p className="text-xs text-gray-200 font-medium leading-relaxed">
                    &quot;{claim.statement}&quot;
                  </p>
                </div>

                {/* Sources Section */}
                {claim.sources && claim.sources.length > 0 && (
                  <div className="space-y-1 pt-2 border-t border-white/5">
                    <p className="text-[10px] text-gray-400 font-mono">Verified Sources:</p>
                    <div className="space-y-1">
                      {claim.sources.slice(0, 2).map((src, sIdx) => (
                        <div key={sIdx} className="flex items-center justify-between text-[11px] text-gray-300">
                          <span className="truncate max-w-[200px] hover:text-sky-300">
                            {getRelationshipBadge(src.relationship)} {src.title || src.source_domain || 'Source'}
                          </span>
                          {src.url && (
                            <a
                              href={src.url}
                              target="_blank"
                              rel="noreferrer"
                              onClick={(e) => e.stopPropagation()}
                              className="text-sky-400 hover:text-sky-300"
                            >
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Skeptic Challenge Callout */}
                {challenge && (
                  <div className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-500/30 text-[11px] space-y-1">
                    <div className="flex items-center justify-between text-rose-300 font-bold font-mono text-[10px]">
                      <span className="flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" /> Skeptic Challenge
                      </span>
                      <span>{challenge.severity}</span>
                    </div>
                    <p className="text-rose-200/80 text-[10px] line-clamp-2">
                      {challenge.counter_argument}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
