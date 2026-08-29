"use client";

import { useInvestigationState } from '@/hooks/useInvestigationState';
import { Suspense, lazy, useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';
import EvidenceMatrix from '@/components/EvidenceMatrix';
import FinalVerdictReport from '@/components/FinalVerdictReport';
import TelemetryStream from '@/components/TelemetryStream';
import InvestigationGraph2D from '@/components/investigation/InvestigationGraph2D';

const Canvas = lazy(() => import('@react-three/fiber').then(m => ({ default: m.Canvas })));
const InvestigationScene = lazy(() => import('@/components/three/InvestigationScene'));
const OrbitControls = lazy(() => import('@react-three/drei').then(m => ({ default: m.OrbitControls })));

function useVisualCapability() {
  const [capability, setCapability] = useState<'FULL_3D' | 'REDUCED_3D' | '2D_FALLBACK'>('FULL_3D');

  useEffect(() => {
    const isMobile = window.innerWidth < 768;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    // Very basic WebGL check
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    const hasWebGL = !!gl;

    if (!hasWebGL || isMobile) {
      setCapability('2D_FALLBACK');
    } else if (reducedMotion) {
      setCapability('REDUCED_3D');
    } else {
      setCapability('FULL_3D');
    }
  }, []);

  return capability;
}

export default function WorkspacePage({ params }: { params: { id: string } }) {
  const state = useInvestigationState(params.id);
  const visualCapability = useVisualCapability();
  
  return (
    <main className="min-h-screen bg-black text-white flex flex-col xl:flex-row font-sans overflow-hidden xl:h-screen">
      
      {/* LEFT PANEL: Investigation Visualization */}
      <section className="relative w-full xl:w-1/2 h-[45vh] sm:h-[50vh] xl:h-full border-b xl:border-b-0 xl:border-r border-neutral-900 bg-neutral-950 flex flex-col shrink-0">
        <div className="absolute top-0 left-0 p-4 xl:p-6 z-10 w-full bg-gradient-to-b from-black/80 to-transparent pointer-events-none">
          <h2 className="text-xs xl:text-sm tracking-[0.2em] text-neutral-500 font-semibold uppercase">Verdict Workspace</h2>
          <div className="flex items-center gap-3 mt-1 xl:mt-2">
            <span className={`h-2 w-2 rounded-full ${state.isConnected ? 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]' : state.isComplete ? 'bg-blue-500' : 'bg-yellow-500 animate-pulse'}`}></span>
            <span className="font-mono text-xs xl:text-sm">{state.isComplete ? 'COMPLETED' : state.isConnected ? 'LIVE' : 'CONNECTING'} {'//'} ROUND {state.round}</span>
          </div>
        </div>

        <div className="flex-1 w-full h-full cursor-grab active:cursor-grabbing">
          {visualCapability === '2D_FALLBACK' ? (
            <InvestigationGraph2D state={state} />
          ) : (
            <Suspense fallback={<div className="w-full h-full flex items-center justify-center text-neutral-600"><Loader2 className="animate-spin w-8 h-8" /></div>}>
              <Canvas camera={{ position: [0, 2, 8], fov: 60 }}>
                <InvestigationScene state={state} />
                <OrbitControls enableZoom={true} enablePan={false} maxPolarAngle={Math.PI / 1.5} minPolarAngle={Math.PI / 4} />
              </Canvas>
            </Suspense>
          )}
        </div>
      </section>

      {/* RIGHT PANEL: Data & UI */}
      <section className="w-full xl:w-1/2 flex-1 overflow-y-auto bg-[#0a0a0a] flex flex-col relative">
        {state.isComplete && state.finalVerdict ? (
          <div className="p-4 xl:p-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
             <FinalVerdictReport verdict={state.finalVerdict} objective={state.objective} />
          </div>
        ) : (
          <div className="flex-1 p-4 xl:p-6 space-y-6 flex flex-col h-full">
            
            {/* TELEMETRY */}
            <div className="h-64 shrink-0">
               <TelemetryStream events={state.events} isConnected={state.isConnected} />
            </div>

            {/* EVIDENCE MATRIX */}
            <div>
               <h3 className="text-[10px] xl:text-xs uppercase tracking-wider text-neutral-500 font-bold mb-3 border-b border-neutral-800 pb-2">Evidence Matrix</h3>
               <EvidenceMatrix claims={state.claims} challenges={state.challenges} />
            </div>
          </div>
        )}
      </section>
      
    </main>
  );
}
