import React from 'react';
import { Settings as SettingsIcon, Server, Cpu } from 'lucide-react';

export const Settings: React.FC = () => {
  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-3xl font-extrabold text-white">Platform Settings</h2>
        <p className="text-slate-400 mt-1">Configure LLM providers, database connections, and model parameters.</p>
      </div>

      <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6 space-y-6">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Cpu className="w-5 h-5 text-indigo-400" /> Pluggable LLM Provider
        </h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-slate-900 border border-indigo-500 rounded-xl">
            <span className="font-bold text-indigo-400 block">Mock Provider (Built-in)</span>
            <span className="text-xs text-slate-400">Default offline intelligent response generator.</span>
          </div>
          <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-xl opacity-60">
            <span className="font-bold text-slate-300 block">OpenAI (GPT-4o)</span>
            <span className="text-xs text-slate-400">Requires OPENAI_API_KEY env var.</span>
          </div>
        </div>
      </div>
    </div>
  );
};
