"use client";

import React, { useRef, useEffect } from 'react';
import { Terminal, CheckCircle2, AlertTriangle, Search, Activity, Cpu } from 'lucide-react';
import { SSEEvent } from '../hooks/useInvestigationSSE';

interface TelemetryStreamProps {
  events: SSEEvent[];
  isConnected: boolean;
}

export default function TelemetryStream({ events, isConnected }: TelemetryStreamProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [events]);

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'ROUND_START':
        return <Activity className="w-4 h-4 text-indigo-400" />;
      case 'LEAD_PLAN_CREATED':
        return <Cpu className="w-4 h-4 text-indigo-400" />;
      case 'RESEARCH_COMPLETED':
        return <Search className="w-4 h-4 text-sky-400" />;
      case 'SKEPTIC_ATTACK_COMPLETED':
        return <AlertTriangle className="w-4 h-4 text-rose-400" />;
      case 'VERIFICATION_COMPLETED':
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      default:
        return <Terminal className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className="flex flex-col h-full glass-panel rounded-2xl border border-white/10 overflow-hidden">
      {/* Panel Header */}
      <div className="px-4 py-3 border-b border-white/10 flex items-center justify-between bg-[#0D0F17]/80">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-indigo-400" />
          <h3 className="text-xs font-bold text-gray-200 uppercase tracking-wider font-mono">
            Execution Telemetry Stream
          </h3>
        </div>

        <div className="flex items-center gap-2">
          <span
            className={`w-2 h-2 rounded-full ${
              isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'
            }`}
          />
          <span className="text-[10px] text-gray-400 font-mono">
            {isConnected ? 'SSE LIVE' : 'CONNECTING'}
          </span>
        </div>
      </div>

      {/* Events Log List */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3 font-mono text-xs">
        {events.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-2 py-12">
            <div className="w-5 h-5 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
            <p className="text-[11px]">Awaiting telemetry stream events...</p>
          </div>
        ) : (
          events.map((evt, idx) => (
            <div
              key={idx}
              className="p-3 rounded-xl bg-[#0D0F17]/90 border border-white/5 space-y-1 hover:border-white/15 transition-all"
            >
              <div className="flex items-center justify-between text-[11px]">
                <span className="flex items-center gap-1.5 font-semibold text-gray-300">
                  {getEventIcon(evt.event_type)}
                  {evt.event_type}
                </span>
                <span className="text-gray-500 text-[10px]">
                  {evt.timestamp ? new Date(evt.timestamp).toLocaleTimeString() : 'NOW'}
                </span>
              </div>

              <p className="text-gray-400 text-[11px] font-sans line-clamp-2">
                {String(evt.data?.summary || evt.data?.description || evt.data?.objective || (evt.data?.role ? `Agent role: ${evt.data.role}` : '') || JSON.stringify(evt.data))}
              </p>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
