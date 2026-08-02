import React, { useEffect, useState } from 'react';
import { fetchApi } from '../api/client';
import { Code, GitCommit, Layers, AlertTriangle } from 'lucide-react';

export const Overview: React.FC = () => {
  const [stats, setStats] = useState({ files: 8, commits: 5, score: 92, status: 'Indexed' });

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-3xl font-extrabold text-white">Repository Overview</h2>
          <p className="text-slate-400 mt-1">Indexed project stats, architecture components, and health summary.</p>
        </div>
        <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm rounded-full font-medium flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          System Online
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-sm font-medium">Source Files</span>
            <Code className="w-5 h-5 text-indigo-400" />
          </div>
          <p className="text-3xl font-bold text-white">{stats.files}</p>
        </div>
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-sm font-medium">Total Commits</span>
            <GitCommit className="w-5 h-5 text-cyan-400" />
          </div>
          <p className="text-3xl font-bold text-white">{stats.commits}</p>
        </div>
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-sm font-medium">Maintainability</span>
            <Layers className="w-5 h-5 text-emerald-400" />
          </div>
          <p className="text-3xl font-bold text-white">{stats.score}%</p>
        </div>
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-sm font-medium">Technical Debt Score</span>
            <AlertTriangle className="w-5 h-5 text-amber-400" />
          </div>
          <p className="text-3xl font-bold text-amber-400">8.0 / 100</p>
        </div>
      </div>

      <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-6 space-y-4">
        <h3 className="text-lg font-bold text-white">Sample Repository Components</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
            <h4 className="font-semibold text-indigo-400">Authentication Service</h4>
            <p className="text-sm text-slate-400 mt-1">JWT Bearer tokens & OAuth2 credential verification.</p>
          </div>
          <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
            <h4 className="font-semibold text-cyan-400">Redis Cache Layer</h4>
            <p className="text-sm text-slate-400 mt-1">TTL-cached session management and query response storage.</p>
          </div>
          <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
            <h4 className="font-semibold text-emerald-400">Payment Processor</h4>
            <p className="text-sm text-slate-400 mt-1">Checkout session workflow & webhook event processing.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
