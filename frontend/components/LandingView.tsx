"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { startInvestigation } from '@/lib/api';
import { ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LandingView() {
  const [objective, setObjective] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!objective.trim() || loading) return;

    setLoading(true);
    try {
      const res = await startInvestigation({ objective, constraints: [] });
      router.push(`/workspace/${res.investigation_id}`);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6 selection:bg-neutral-800">
      <div className="w-full max-w-2xl mx-auto space-y-12">
        
        <div className="text-center space-y-4">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl md:text-7xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-white to-neutral-600"
          >
            VERDICT
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-lg md:text-xl text-neutral-400 font-light"
          >
            Research. Challenge. Verify. Decide.
          </motion.p>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="relative"
        >
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-orange-500/20 rounded-2xl blur-lg"></div>
          <form onSubmit={handleStart} className="relative bg-neutral-900/80 backdrop-blur-xl border border-neutral-800 rounded-2xl p-2 shadow-2xl flex items-center transition-all focus-within:border-neutral-600 focus-within:ring-4 focus-within:ring-white/5">
            <textarea
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              placeholder="What do you need to investigate?"
              disabled={loading}
              className="w-full bg-transparent resize-none p-4 text-lg text-white placeholder-neutral-500 focus:outline-none min-h-[60px] leading-relaxed"
              rows={1}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleStart(e);
                }
              }}
            />
            <button
              type="submit"
              disabled={loading || !objective.trim()}
              className="m-2 p-4 bg-white text-black rounded-xl hover:bg-neutral-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : <ArrowRight className="w-6 h-6" />}
            </button>
          </form>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="flex flex-col items-center gap-4 text-sm text-neutral-500"
        >
          <span className="uppercase tracking-widest text-xs font-semibold">Example Investigations</span>
          <div className="flex flex-wrap justify-center gap-3">
            {[
              "What should I build for this hackathon?",
              "Is this startup idea genuinely differentiated?",
              "Should I use PostgreSQL or MongoDB for my app?"
            ].map(q => (
              <button 
                key={q} 
                onClick={() => setObjective(q)}
                className="px-4 py-2 rounded-full border border-neutral-800 hover:border-neutral-600 hover:text-neutral-300 transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

// Inline Loader since we used it
function Loader2({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
  );
}
