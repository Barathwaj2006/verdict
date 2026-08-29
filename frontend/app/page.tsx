"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { startInvestigation } from '@/lib/api';

export default function Home() {
  const [objective, setObjective] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!objective.trim()) {
      setError('Please enter an objective.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await startInvestigation({ objective, constraints: [] });
      router.push(`/investigate/${res.investigation_id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to start investigation');
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-neutral-900 text-white flex flex-col items-center justify-center p-4">
      <div className="max-w-3xl w-full space-y-8 text-center">
        <h1 className="text-5xl font-bold tracking-tight">VERDICT</h1>
        <p className="text-xl text-neutral-400">
          Don't just ask AI what to build. <br/>
          Ask VERDICT what deserves to be built.
        </p>

        <form onSubmit={handleStart} className="space-y-4">
          <textarea
            className="w-full bg-neutral-800 border border-neutral-700 rounded-lg p-4 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
            placeholder="What decision do you need evidence for? e.g. Find the strongest project idea for this hackathon..."
            value={objective}
            onChange={e => setObjective(e.target.value)}
            disabled={loading}
          />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Starting Investigation...' : 'Start Investigation'}
          </button>
        </form>

        <div className="text-left text-neutral-500 text-sm mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 className="font-semibold text-neutral-300 mb-2">Multi-Agent Research</h3>
            <p>VERDICT spins up specialized agents to parallelize fact-finding across diverse sources.</p>
          </div>
          <div>
            <h3 className="font-semibold text-neutral-300 mb-2">Adversarial Skepticism</h3>
            <p>Every claim is actively challenged by the Skeptic to identify weak assumptions.</p>
          </div>
          <div>
            <h3 className="font-semibold text-neutral-300 mb-2">Independent Verification</h3>
            <p>Disputed claims are adjudicated by an isolated Verifier drawing on fresh evidence.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
