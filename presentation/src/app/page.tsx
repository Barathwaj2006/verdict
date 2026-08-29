"use client";

import { motion } from "framer-motion";
import { ArrowRight, Brain, Search, Shield, ChevronDown, CheckCircle2, AlertTriangle, Layers, Zap, SearchCode, Database, Activity } from "lucide-react";
import Link from "next/link";

export default function Presentation() {
  return (
    <div className="min-h-screen bg-[#050505] text-white selection:bg-neutral-800 font-sans">
      {/* NAVIGATION */}
      <nav className="fixed top-0 w-full z-50 bg-[#050505]/80 backdrop-blur-xl border-b border-neutral-900">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="font-bold tracking-widest text-lg">VERDICT</div>
          <div className="hidden md:flex gap-6 text-sm text-neutral-400">
            <a href="#problem" className="hover:text-white transition-colors">Problem</a>
            <a href="#how-it-works" className="hover:text-white transition-colors">How It Works</a>
            <a href="#investigation" className="hover:text-white transition-colors">Investigation</a>
            <a href="#evidence" className="hover:text-white transition-colors">Evidence</a>
            <a href="#architecture" className="hover:text-white transition-colors">Architecture</a>
          </div>
          <button className="px-4 py-2 bg-white text-black rounded-full text-sm font-semibold hover:bg-neutral-200 transition-colors">
            Launch VERDICT
          </button>
        </div>
      </nav>

      {/* SECTION 1 — HERO */}
      <section className="relative min-h-screen flex flex-col items-center justify-center pt-20 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-[#050505] to-[#050505] -z-10"></div>
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="text-center max-w-4xl px-6 z-10"
        >
          <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-neutral-500">
            AI Can Answer.<br />VERDICT Investigates.
          </h1>
          <p className="text-xl md:text-2xl text-neutral-400 font-light mb-10 max-w-3xl mx-auto leading-relaxed">
            An autonomous research system that plans investigations, challenges its own findings, independently verifies evidence, and keeps researching until a defensible conclusion is earned.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-neutral-200 transition-colors flex items-center justify-center gap-2">
              Launch VERDICT <ArrowRight className="w-5 h-5" />
            </button>
            <a href="#problem" className="px-8 py-4 border border-neutral-700 rounded-full font-semibold text-lg hover:bg-neutral-800 transition-colors flex items-center justify-center">
              See How It Works
            </a>
          </div>
        </motion.div>
        
        {/* Subtle Conceptual Flow */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 2 }}
          className="mt-20 flex items-center gap-4 md:gap-8 text-neutral-500 text-sm font-mono tracking-wider overflow-x-auto max-w-full px-6"
        >
          <span>QUESTION</span>
          <ChevronDown className="w-4 h-4 -rotate-90" />
          <span className="text-white">RESEARCH</span>
          <ChevronDown className="w-4 h-4 -rotate-90" />
          <span className="text-orange-500">CHALLENGE</span>
          <ChevronDown className="w-4 h-4 -rotate-90" />
          <span className="text-blue-500">VERIFY</span>
          <ChevronDown className="w-4 h-4 -rotate-90" />
          <span className="text-green-500 font-bold">VERDICT</span>
        </motion.div>
      </section>

      {/* SECTION 2 — THE PROBLEM */}
      <section id="problem" className="py-32 px-6 bg-neutral-950">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-16">The Hardest Part Isn't Getting an Answer.</h2>
          <div className="grid md:grid-cols-2 gap-12 text-left">
            <div>
              <h3 className="text-2xl font-semibold mb-4 text-neutral-300">Modern AI makes it easy to generate:</h3>
              <ul className="space-y-3 text-neutral-500 text-lg">
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5" /> ideas</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5" /> summaries</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5" /> explanations</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5" /> code</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5" /> recommendations</li>
              </ul>
            </div>
            <div>
              <h3 className="text-2xl font-semibold mb-4 text-neutral-300">But difficult decisions require people to:</h3>
              <ul className="space-y-3 text-neutral-500 text-lg">
                <li className="flex items-center gap-3"><AlertTriangle className="w-5 h-5" /> determine what needs to be researched</li>
                <li className="flex items-center gap-3"><AlertTriangle className="w-5 h-5" /> find relevant evidence</li>
                <li className="flex items-center gap-3"><AlertTriangle className="w-5 h-5" /> challenge assumptions</li>
                <li className="flex items-center gap-3"><AlertTriangle className="w-5 h-5" /> verify claims & resolve contradictions</li>
                <li className="flex items-center gap-3"><AlertTriangle className="w-5 h-5" /> determine if enough evidence exists</li>
              </ul>
            </div>
          </div>
          <div className="mt-20 p-8 border border-neutral-800 bg-neutral-900/50 rounded-2xl">
            <div className="flex flex-col md:flex-row items-center justify-center gap-6 font-mono text-sm text-neutral-400 mb-8">
              <span>QUESTION</span> <ArrowRight className="w-4 h-4 hidden md:block" />
              <span>LLM</span> <ArrowRight className="w-4 h-4 hidden md:block" />
              <span>ANSWER</span> <ArrowRight className="w-4 h-4 hidden md:block" />
              <span className="text-red-500">???</span>
            </div>
            <p className="text-2xl font-light text-white">"An answer is not the same thing as an investigated conclusion."</p>
          </div>
        </div>
      </section>

      {/* SECTION 3 — WHY EXISTING AI FALLS SHORT */}
      <section className="py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold mb-16 text-center">Generation Isn't Investigation.</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-neutral-800 text-neutral-400">
                  <th className="p-4 font-normal">Capability</th>
                  <th className="p-4 font-normal">Single LLM</th>
                  <th className="p-4 font-normal">Basic Search + Summary</th>
                  <th className="p-4 font-normal">Static Agent Workflow</th>
                  <th className="p-4 font-semibold text-white">VERDICT</th>
                </tr>
              </thead>
              <tbody className="text-neutral-300">
                <tr className="border-b border-neutral-900/50">
                  <td className="p-4">Planning</td>
                  <td className="p-4 text-neutral-600">None</td>
                  <td className="p-4 text-neutral-600">None</td>
                  <td className="p-4 text-neutral-400">Hardcoded</td>
                  <td className="p-4 text-blue-400 font-medium">Dynamic Missions</td>
                </tr>
                <tr className="border-b border-neutral-900/50">
                  <td className="p-4">Evidence</td>
                  <td className="p-4 text-neutral-600">Internal Weights</td>
                  <td className="p-4 text-neutral-400">Single Pass</td>
                  <td className="p-4 text-neutral-400">Single Pass</td>
                  <td className="p-4 text-blue-400 font-medium">Extracted & Linked</td>
                </tr>
                <tr className="border-b border-neutral-900/50">
                  <td className="p-4">Adversarial Challenge</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">Rarely</td>
                  <td className="p-4 text-orange-400 font-medium">Dedicated Skeptic</td>
                </tr>
                <tr className="border-b border-neutral-900/50">
                  <td className="p-4">Independent Verification</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-green-400 font-medium">Dedicated Verifier</td>
                </tr>
                <tr className="border-b border-neutral-900/50">
                  <td className="p-4">Knowledge-Gap Detection</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-blue-400 font-medium">Explicit Phase</td>
                </tr>
                <tr className="border-b border-neutral-900/50">
                  <td className="p-4">Recursion</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-neutral-600">No</td>
                  <td className="p-4 text-blue-400 font-medium">Yes, until sufficient</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* SECTION 4 — THE INSIGHT */}
      <section className="py-32 px-6 bg-gradient-to-b from-neutral-950 to-[#050505]">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-6xl font-bold mb-8 leading-tight">
            "Don't just ask AI for the answer.<br/>
            Ask it what it needs to know first."
          </h2>
          <p className="text-xl text-neutral-400 font-light leading-relaxed">
            VERDICT treats a decision as an investigation.<br/><br/>
            The system first determines: <em>"What must be true before I can responsibly conclude?"</em><br/>
            Then, it dynamically designs the research required to answer exactly that question.
          </p>
        </div>
      </section>

      {/* SECTION 5 — WHAT VERDICT DOES */}
      <section id="how-it-works" className="py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold mb-16 text-center">Meet the Investigation Engine.</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="p-8 border border-neutral-800 bg-neutral-900/30 rounded-2xl">
              <Brain className="w-10 h-10 text-blue-400 mb-6" />
              <h3 className="text-2xl font-bold mb-2">1. LEAD</h3>
              <p className="text-sm text-blue-400 font-mono mb-4">"The Strategist"</p>
              <p className="text-neutral-400">Plans the investigation. Determines what needs to be known. Creates dynamic research missions. Decides whether evidence is sufficient.</p>
            </div>
            <div className="p-8 border border-neutral-800 bg-neutral-900/30 rounded-2xl">
              <Search className="w-10 h-10 text-purple-400 mb-6" />
              <h3 className="text-2xl font-bold mb-2">2. SPECIALISTS</h3>
              <p className="text-sm text-purple-400 font-mono mb-4">"The Investigators"</p>
              <p className="text-neutral-400">Receive dynamically generated missions. Search external sources in parallel. Extract claims and structured evidence.</p>
            </div>
            <div className="p-8 border border-neutral-800 bg-neutral-900/30 rounded-2xl">
              <AlertTriangle className="w-10 h-10 text-orange-400 mb-6" />
              <h3 className="text-2xl font-bold mb-2">3. SKEPTIC</h3>
              <p className="text-sm text-orange-400 font-mono mb-4">"The Adversary"</p>
              <p className="text-neutral-400">Attempts to break important claims. Searches for contradictions, counterexamples, weak evidence, missing context, and hidden assumptions.</p>
            </div>
            <div className="p-8 border border-neutral-800 bg-neutral-900/30 rounded-2xl">
              <Shield className="w-10 h-10 text-green-400 mb-6" />
              <h3 className="text-2xl font-bold mb-2">4. VERIFIER</h3>
              <p className="text-sm text-green-400 font-mono mb-4">"The Adjudicator"</p>
              <p className="text-neutral-400">Independently investigates disputed claims. Builds a rigorous evidence matrix. Determines what the evidence actually establishes.</p>
            </div>
            <div className="p-8 border border-neutral-800 bg-neutral-900/30 rounded-2xl lg:col-span-2">
              <Activity className="w-10 h-10 text-white mb-6" />
              <h3 className="text-2xl font-bold mb-2">5. RECURSIVE CONTROLLER</h3>
              <p className="text-sm text-neutral-400 font-mono mb-4">"The Decision Loop"</p>
              <p className="text-neutral-400">Evaluates the aggregate evidence state and determines whether another research round is necessary to close critical knowledge gaps before concluding.</p>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 6 — DYNAMIC AGENT ORCHESTRATION */}
      <section className="py-32 px-6 bg-neutral-950">
        <div className="max-w-5xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">The Team Is Generated by the Question.</h2>
          <p className="text-xl text-neutral-400 mb-16">There is no fixed "Agent 1, Agent 2, Agent 3". The Lead asks: <em>"What expertise does this problem require?"</em></p>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="border border-neutral-800 p-6 rounded-xl text-left bg-black">
              <p className="text-sm font-mono text-neutral-500 mb-4">Example A: Hackathon Idea</p>
              <ul className="space-y-2 text-blue-300">
                <li>→ Landscape Researcher</li>
                <li>→ Feasibility Analyst</li>
                <li>→ Opportunity Scout</li>
                <li>→ Competition Tracker</li>
              </ul>
            </div>
            <div className="border border-neutral-800 p-6 rounded-xl text-left bg-black">
              <p className="text-sm font-mono text-neutral-500 mb-4">Example B: Architecture Decision</p>
              <ul className="space-y-2 text-purple-300">
                <li>→ Performance Expert</li>
                <li>→ Cost Analyst</li>
                <li>→ Migration Specialist</li>
                <li>→ Security Auditor</li>
              </ul>
            </div>
            <div className="border border-neutral-800 p-6 rounded-xl text-left bg-black">
              <p className="text-sm font-mono text-neutral-500 mb-4">Example C: Scientific Question</p>
              <ul className="space-y-2 text-green-300">
                <li>→ Literature Reviewer</li>
                <li>→ Methodology Critic</li>
                <li>→ Evidence Quality Analyst</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 7 — THE RECURSIVE INVESTIGATION */}
      <section id="investigation" className="py-32 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-16">VERDICT Knows When It Doesn't Know Enough.</h2>
          
          <div className="bg-neutral-900/40 border border-neutral-800 rounded-3xl p-8 md:p-16">
            <div className="flex flex-col items-center">
              <div className="px-4 py-1 border border-neutral-700 rounded-full text-xs font-mono mb-8">ROUND 1</div>
              <div className="flex gap-4 mb-8 text-neutral-400 font-mono text-sm">
                <span>Lead</span> <ArrowRight className="w-4 h-4"/> <span>Research</span> <ArrowRight className="w-4 h-4"/> <span>Skeptic</span> <ArrowRight className="w-4 h-4"/> <span>Verifier</span>
              </div>
              
              <div className="w-full max-w-md bg-red-950/30 border border-red-900/50 text-red-400 p-6 rounded-xl mb-8 flex flex-col items-center">
                <AlertTriangle className="w-8 h-8 mb-4" />
                <span className="font-bold tracking-widest text-sm mb-2">KNOWLEDGE GAP IDENTIFIED</span>
                <span className="text-center text-red-300/80">"Primary-source evidence regarding performance benchmarks is still missing."</span>
              </div>
              
              <div className="w-px h-16 bg-gradient-to-b from-red-900/50 to-blue-900/50 mb-8"></div>
              
              <div className="px-4 py-1 border border-neutral-700 rounded-full text-xs font-mono mb-8">ROUND 2: FOLLOW-UP MISSION</div>
              <div className="flex gap-4 mb-8 text-neutral-400 font-mono text-sm">
                <span>Research</span> <ArrowRight className="w-4 h-4"/> <span>Skeptic</span> <ArrowRight className="w-4 h-4"/> <span>Verifier</span> <ArrowRight className="w-4 h-4"/> <span>Lead</span>
              </div>

              <div className="w-full max-w-md bg-green-950/30 border border-green-900/50 text-green-400 p-6 rounded-xl flex flex-col items-center">
                <CheckCircle2 className="w-8 h-8 mb-4" />
                <span className="font-bold tracking-widest text-sm mb-2">EVIDENCE THRESHOLD REACHED</span>
                <span className="text-center text-green-300/80">Proceed to Final Verdict.</span>
              </div>
            </div>
          </div>
          <p className="mt-8 text-neutral-400 text-lg">
            The system does not blindly repeat the same workflow. The next research round is explicitly generated to resolve missing evidence.
          </p>
        </div>
      </section>

      {/* SECTION 8 — EVIDENCE INTEGRITY */}
      <section id="evidence" className="py-32 px-6 bg-neutral-950">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 text-center">We Don't Trust the Model.</h2>
          <p className="text-xl text-neutral-400 text-center mb-16">
            Safeguards exist <em>outside</em> the model. Hallucinated URLs are instantly rejected. Claims begin UNVERIFIED.
          </p>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="border border-neutral-800 bg-black p-8 rounded-2xl">
              <h3 className="text-sm font-mono text-neutral-500 mb-6">INTEGRITY ENFORCEMENT</h3>
              <ul className="space-y-4 text-neutral-300">
                <li className="flex gap-3">
                  <Shield className="w-5 h-5 text-neutral-500 shrink-0" /> 
                  <span>External URLs must originate strictly from retrieved search results.</span>
                </li>
                <li className="flex gap-3">
                  <Shield className="w-5 h-5 text-neutral-500 shrink-0" /> 
                  <span>Verification explicitly requires evidence.</span>
                </li>
                <li className="flex gap-3">
                  <Shield className="w-5 h-5 text-neutral-500 shrink-0" /> 
                  <span>Conflicting evidence remains contested.</span>
                </li>
                <li className="flex gap-3">
                  <Shield className="w-5 h-5 text-neutral-500 shrink-0" /> 
                  <span>Internal model knowledge is flagged and distinguished from external evidence.</span>
                </li>
              </ul>
            </div>
            
            <div className="border border-red-900/30 bg-red-950/10 p-8 rounded-2xl flex flex-col justify-center">
              <div className="text-sm font-mono text-neutral-500 mb-2">MODEL CLAIM:</div>
              <div className="p-4 bg-neutral-900 rounded mb-4 text-white">"This source at fake-url.com proves X."</div>
              <div className="text-sm font-mono text-neutral-500 mb-2">SYSTEM PROTECTOR:</div>
              <div className="p-4 border border-red-900/50 bg-red-950/30 text-red-400 rounded flex items-center justify-between">
                <span>Source not retrieved.</span>
                <span className="font-bold tracking-widest text-xs">→ REJECTED</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 9 — EVIDENCE MATRIX */}
      <section className="py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold mb-12 text-center">The Evidence Matrix</h2>
          <div className="overflow-x-auto border border-neutral-800 rounded-xl">
            <table className="w-full text-left bg-neutral-900/20">
              <thead className="bg-neutral-900/80 text-xs font-mono tracking-widest text-neutral-500">
                <tr>
                  <th className="p-4">CLAIM</th>
                  <th className="p-4">SOURCE</th>
                  <th className="p-4">RELATIONSHIP</th>
                  <th className="p-4">RELEVANCE</th>
                  <th className="p-4">STATUS</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                <tr className="border-t border-neutral-800">
                  <td className="p-4 text-white max-w-xs">PostgreSQL outperforms MongoDB in highly relational queries.</td>
                  <td className="p-4 text-neutral-400">docs.postgresql.org</td>
                  <td className="p-4"><span className="text-green-400 bg-green-400/10 px-2 py-1 rounded text-xs font-bold">SUPPORTS</span></td>
                  <td className="p-4 text-neutral-400">High</td>
                  <td className="p-4"><span className="text-green-400 font-mono">VERIFIED</span></td>
                </tr>
                <tr className="border-t border-neutral-800">
                  <td className="p-4 text-white max-w-xs">MongoDB is faster for unstructured JSON writes.</td>
                  <td className="p-4 text-neutral-400">blog.mongodb.com</td>
                  <td className="p-4"><span className="text-orange-400 bg-orange-400/10 px-2 py-1 rounded text-xs font-bold">QUALIFIES</span></td>
                  <td className="p-4 text-neutral-400">Medium</td>
                  <td className="p-4"><span className="text-orange-400 font-mono">CONTESTED</span></td>
                </tr>
                <tr className="border-t border-neutral-800">
                  <td className="p-4 text-white max-w-xs">NoSQL databases are obsolete.</td>
                  <td className="p-4 text-neutral-400">random-tech-blog.dev</td>
                  <td className="p-4"><span className="text-red-400 bg-red-400/10 px-2 py-1 rounded text-xs font-bold">CONTRADICTS</span></td>
                  <td className="p-4 text-neutral-400">Low</td>
                  <td className="p-4"><span className="text-red-400 font-mono">REFUTED</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="text-center text-xs text-neutral-600 mt-4 font-mono">* Example matrix illustrating VERDICT's internal evaluation structures.</p>
        </div>
      </section>

      {/* SECTION 10 — REAL-TIME INVESTIGATION */}
      <section className="py-32 px-6 bg-neutral-950 overflow-hidden">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-16">Watch the Investigation Happen.</h2>
          <div className="relative border-l border-neutral-800 ml-4 md:ml-0 md:mx-auto max-w-lg text-left pl-8 pb-8 space-y-8 font-mono text-sm">
            <div className="relative">
              <div className="absolute -left-[41px] top-1 w-3 h-3 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.8)]"></div>
              <div className="text-neutral-500 mb-1">10:42</div>
              <div className="text-white">Lead created research plan</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[41px] top-1 w-3 h-3 rounded-full bg-purple-500"></div>
              <div className="text-neutral-500 mb-1">10:43</div>
              <div className="text-white">4 specialist missions launched</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[41px] top-1 w-3 h-3 rounded-full bg-neutral-500"></div>
              <div className="text-neutral-500 mb-1">10:44</div>
              <div className="text-white">27 sources discovered</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[41px] top-1 w-3 h-3 rounded-full bg-orange-500"></div>
              <div className="text-neutral-500 mb-1">10:45</div>
              <div className="text-white">Skeptic challenged 3 claims</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[41px] top-1 w-3 h-3 rounded-full bg-red-500"></div>
              <div className="text-neutral-500 mb-1">10:47</div>
              <div className="text-white">Evidence insufficient. Knowledge gap logged.</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[41px] top-1 w-3 h-3 rounded-full bg-blue-500"></div>
              <div className="text-neutral-500 mb-1">10:48</div>
              <div className="text-white">Round 2 launched</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[41px] top-1 w-3 h-3 rounded-full bg-green-500 shadow-[0_0_15px_rgba(34,197,94,0.8)]"></div>
              <div className="text-neutral-500 mb-1">10:50</div>
              <div className="text-green-400 font-bold">Evidence threshold reached</div>
            </div>
          </div>
          
          <button className="mt-16 px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-neutral-200 transition-colors">
            Open the Live Investigation
          </button>
        </div>
      </section>

      {/* SECTION 11 — BEFORE / AFTER */}
      <section className="py-32 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-light mb-16 leading-tight">
            "Most AI systems optimize for answers.<br/>
            <span className="font-bold">VERDICT optimizes for defensible conclusions.</span>"
          </h2>
          
          <div className="grid md:grid-cols-2 gap-16 font-mono text-sm">
            <div className="flex flex-col items-center">
              <div className="text-neutral-500 mb-8 tracking-widest">TRADITIONAL AI</div>
              <div className="w-full max-w-xs border border-neutral-800 p-6 rounded-xl space-y-4 bg-neutral-900/20 text-neutral-400">
                <div>Question</div>
                <ChevronDown className="w-4 h-4 mx-auto" />
                <div>Generate</div>
                <ChevronDown className="w-4 h-4 mx-auto" />
                <div className="text-white font-bold">Answer</div>
              </div>
            </div>
            
            <div className="flex flex-col items-center">
              <div className="text-white mb-8 tracking-widest font-bold">VERDICT</div>
              <div className="w-full max-w-xs border border-blue-900/50 p-6 rounded-xl space-y-4 bg-blue-950/10 text-neutral-300">
                <div>Question</div>
                <ChevronDown className="w-4 h-4 mx-auto text-blue-500" />
                <div>Plan</div>
                <ChevronDown className="w-4 h-4 mx-auto text-blue-500" />
                <div>Research</div>
                <ChevronDown className="w-4 h-4 mx-auto text-orange-500" />
                <div className="text-orange-400">Challenge</div>
                <ChevronDown className="w-4 h-4 mx-auto text-green-500" />
                <div className="text-green-400">Verify</div>
                <ChevronDown className="w-4 h-4 mx-auto text-blue-500" />
                <div>Measure uncertainty</div>
                <ChevronDown className="w-4 h-4 mx-auto text-blue-500" />
                <div>Research again</div>
                <ChevronDown className="w-4 h-4 mx-auto text-green-500" />
                <div className="text-white font-bold">Defensible conclusion</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 12 — GOOGLE TECHNOLOGY */}
      <section className="py-32 px-6 bg-neutral-950">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold mb-16 text-center">Built Around Google's AI & Cloud Stack.</h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="border border-neutral-800 p-8 rounded-2xl bg-black">
              <h3 className="text-xl font-bold mb-4 text-white">Gemini</h3>
              <p className="text-neutral-400">Powers reasoning, planning, research synthesis, rigorous skepticism, independent verification, and final evaluation.</p>
            </div>
            <div className="border border-neutral-800 p-8 rounded-2xl bg-black">
              <h3 className="text-xl font-bold mb-4 text-white">Google GenAI SDK</h3>
              <p className="text-neutral-400">Facilitates highly structured agent/model interaction and reliable parallel execution.</p>
            </div>
            <div className="border border-neutral-800 p-8 rounded-2xl bg-black">
              <h3 className="text-xl font-bold mb-4 text-white">Firestore</h3>
              <p className="text-neutral-400">Provides persistent, scalable storage for investigation state, matrices, and recovery snapshots.</p>
            </div>
            <div className="border border-neutral-800 p-8 rounded-2xl bg-black">
              <h3 className="text-xl font-bold mb-4 text-white">Cloud Run</h3>
              <p className="text-neutral-400">The FastAPI backend is entirely deployment-ready for Google Cloud Run containerized environments.</p>
            </div>
            <div className="border border-neutral-800 p-8 rounded-2xl bg-black lg:col-span-2">
              <h3 className="text-xl font-bold mb-4 text-white">SSE / EventBus</h3>
              <p className="text-neutral-400">Streams live investigation telemetry to the interactive Next.js 3D dashboard in real time.</p>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 13 — TECHNICAL ARCHITECTURE */}
      <section id="architecture" className="py-32 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-4xl font-bold mb-12 text-center">System Architecture</h2>
          <div className="w-full bg-neutral-900 border border-neutral-800 rounded-3xl p-8 md:p-12">
            
            {/* Layer 1 */}
            <div className="mb-6 border border-neutral-700/50 rounded-xl p-4 bg-neutral-950">
              <div className="text-xs font-mono text-neutral-500 mb-4">1. INTERACTION</div>
              <div className="flex gap-4 flex-wrap">
                <span className="px-3 py-1 bg-neutral-800 rounded text-sm">Next.js</span>
                <span className="px-3 py-1 bg-neutral-800 rounded text-sm">Chat Interface</span>
                <span className="px-3 py-1 bg-neutral-800 rounded text-sm">Investigation Workspace</span>
              </div>
            </div>

            {/* Layer 2 */}
            <div className="mb-6 border border-neutral-700/50 rounded-xl p-4 bg-neutral-950">
              <div className="text-xs font-mono text-neutral-500 mb-4">2. CONTROL</div>
              <div className="flex gap-4 flex-wrap">
                <span className="px-3 py-1 bg-blue-900/30 text-blue-300 rounded text-sm">FastAPI</span>
                <span className="px-3 py-1 bg-blue-900/30 text-blue-300 rounded text-sm">Lead Agent</span>
                <span className="px-3 py-1 bg-blue-900/30 text-blue-300 rounded text-sm">Controller</span>
                <span className="px-3 py-1 bg-blue-900/30 text-blue-300 rounded text-sm">Dynamic Planner</span>
              </div>
            </div>

            {/* Layer 3 */}
            <div className="mb-6 border border-neutral-700/50 rounded-xl p-4 bg-neutral-950">
              <div className="text-xs font-mono text-neutral-500 mb-4">3. AGENT EXECUTION</div>
              <div className="flex gap-4 flex-wrap">
                <span className="px-3 py-1 bg-purple-900/30 text-purple-300 rounded text-sm">Specialist Researchers</span>
                <span className="px-3 py-1 bg-orange-900/30 text-orange-300 rounded text-sm">Skeptic</span>
                <span className="px-3 py-1 bg-green-900/30 text-green-300 rounded text-sm">Verifier</span>
              </div>
            </div>

            {/* Layer 4 */}
            <div className="mb-6 border border-neutral-700/50 rounded-xl p-4 bg-neutral-950">
              <div className="text-xs font-mono text-neutral-500 mb-4">4. EVIDENCE / DECISION</div>
              <div className="flex gap-4 flex-wrap">
                <span className="px-3 py-1 bg-neutral-800 rounded text-sm">Research Tool</span>
                <span className="px-3 py-1 bg-neutral-800 rounded text-sm">Evidence Integrity</span>
                <span className="px-3 py-1 bg-neutral-800 rounded text-sm">Matrix</span>
                <span className="px-3 py-1 bg-neutral-800 rounded text-sm">Knowledge Gaps</span>
              </div>
            </div>

            {/* Layer 5 */}
            <div className="border border-neutral-700/50 rounded-xl p-4 bg-neutral-950">
              <div className="text-xs font-mono text-neutral-500 mb-4">5. INFRASTRUCTURE</div>
              <div className="flex gap-4 flex-wrap">
                <span className="px-3 py-1 bg-white text-black font-bold rounded text-sm">Gemini</span>
                <span className="px-3 py-1 bg-white text-black font-bold rounded text-sm">Cloud Run</span>
                <span className="px-3 py-1 bg-white text-black font-bold rounded text-sm">Firestore</span>
                <span className="px-3 py-1 bg-white text-black font-bold rounded text-sm">EventBus/SSE</span>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* SECTION 14 — FINAL VERDICT */}
      <section className="py-32 px-6 bg-neutral-950">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold mb-16 text-center">Not Just an Answer.<br/>A Decision Package.</h2>
          
          <div className="bg-white text-black p-8 md:p-12 rounded-xl shadow-2xl">
            <div className="border-b border-neutral-200 pb-6 mb-6 flex justify-between items-end">
              <div>
                <div className="text-neutral-500 font-mono text-sm mb-2">EXECUTIVE BRIEFING</div>
                <h3 className="text-3xl font-bold">FINAL VERDICT</h3>
              </div>
              <div className="text-right">
                <div className="text-neutral-500 font-mono text-sm mb-1">CONFIDENCE</div>
                <div className="text-3xl font-bold text-green-600">92%</div>
              </div>
            </div>
            
            <div className="space-y-8">
              <div>
                <h4 className="font-bold text-lg mb-2">Recommendation</h4>
                <p className="text-neutral-700">Proceed with building the localized emergency response application. The market opportunity is highly differentiated, technically feasible within 48 hours, and supported by verified API availability.</p>
              </div>
              
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h4 className="font-bold text-sm uppercase text-neutral-500 tracking-wider mb-3">Verified Findings</h4>
                  <ul className="space-y-2 text-sm text-neutral-800 list-disc list-inside">
                    <li>Twilio API supports necessary SMS broadcast volumes.</li>
                    <li>No direct open-source competitors identified.</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-bold text-sm uppercase text-neutral-500 tracking-wider mb-3">Risks & Trade-offs</h4>
                  <ul className="space-y-2 text-sm text-neutral-800 list-disc list-inside">
                    <li>Rate limits on free API tiers.</li>
                    <li>Requires strict data privacy handling.</li>
                  </ul>
                </div>
              </div>

              <div className="bg-neutral-50 p-4 rounded border border-neutral-200 text-sm flex justify-between items-center text-neutral-600 font-mono mt-8">
                <span>Research Rounds: 2</span>
                <span>Evidence Examined: 14 Sources</span>
                <span>Status: CONCLUDED</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 15 — USE CASE */}
      <section className="py-32 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Built for Hackathons.<br/>Designed for Decisions.</h2>
          <p className="text-xl text-neutral-400 mb-16">VERDICT helps identify what is actually worth building.</p>
          
          <div className="flex flex-col md:flex-row gap-4 items-stretch justify-center">
            <div className="flex-1 bg-neutral-900 border border-neutral-800 p-8 rounded-xl flex flex-col justify-center">
              <div className="font-mono text-sm text-neutral-500 mb-4">USER PROVIDES</div>
              <ul className="space-y-2 text-left w-max mx-auto">
                <li>+ Hackathon Details</li>
                <li>+ Constraints</li>
                <li>+ Goals</li>
              </ul>
            </div>
            
            <div className="flex-1 bg-blue-950/20 border border-blue-900/50 p-8 rounded-xl flex flex-col justify-center">
              <div className="font-mono text-sm text-blue-500 mb-4">VERDICT INVESTIGATES</div>
              <ul className="space-y-2 text-left w-max mx-auto text-neutral-300">
                <li>• Requirements</li>
                <li>• Judging Criteria</li>
                <li>• Existing Solutions</li>
                <li>• Differentiation</li>
                <li>• Feasibility</li>
              </ul>
            </div>
            
            <div className="flex-1 bg-green-950/20 border border-green-900/50 p-8 rounded-xl flex flex-col justify-center">
              <div className="font-mono text-sm text-green-500 mb-4">SYSTEM RETURNS</div>
              <ul className="space-y-2 text-left w-max mx-auto text-neutral-300">
                <li>✓ Recommended Idea</li>
                <li>✓ Verified Evidence</li>
                <li>✓ Identified Risks</li>
                <li>✓ Alternatives</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 16 — FUTURE */}
      <section className="py-32 px-6 bg-neutral-950 border-t border-neutral-900">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-8">Research Is Only the Beginning.</h2>
          <div className="flex flex-wrap justify-center gap-4 text-neutral-400">
            <span className="px-4 py-2 bg-neutral-900 rounded-full">Startup Validation</span>
            <span className="px-4 py-2 bg-neutral-900 rounded-full">Architecture Decisions</span>
            <span className="px-4 py-2 bg-neutral-900 rounded-full">Product Strategy</span>
            <span className="px-4 py-2 bg-neutral-900 rounded-full">Technical Due Diligence</span>
            <span className="px-4 py-2 bg-neutral-900 rounded-full">Scientific Research</span>
            <span className="px-4 py-2 bg-neutral-900 rounded-full">Procurement</span>
            <span className="px-4 py-2 bg-neutral-900 rounded-full">Investment Research</span>
          </div>
        </div>
      </section>

      {/* SECTION 17 — FINAL CTA */}
      <section className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-blue-900/20 via-[#050505] to-[#050505] -z-10"></div>
        <div className="text-center z-10 px-6">
          <h2 className="text-6xl md:text-8xl font-bold mb-4 tracking-tighter">Don't Ask AI What It Thinks.</h2>
          <p className="text-3xl md:text-5xl font-light text-neutral-400 mb-16">Ask It to Find Out.</p>
          
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <button className="px-8 py-4 bg-white text-black rounded-full font-bold text-lg hover:bg-neutral-200 transition-colors">
              Launch VERDICT
            </button>
            <button className="px-8 py-4 border border-neutral-700 rounded-full font-bold text-lg hover:bg-neutral-800 transition-colors">
              View GitHub
            </button>
            <button className="px-8 py-4 border border-neutral-700 rounded-full font-bold text-lg hover:bg-neutral-800 transition-colors">
              Watch Demo
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
