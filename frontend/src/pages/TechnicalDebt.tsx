import React, { useEffect, useState } from 'react';
import { fetchApi } from '../api/client';
import { AlertTriangle, CheckCircle, ShieldAlert } from 'lucide-react';

export const TechnicalDebt: React.FC = () => {
  const [debtData, setDebtData] = useState<any>(null);

  useEffect(() => {
    fetchApi('/technical-debt?repo_id=1')
      .then(data => setDebtData(data))
      .catch(console.error);
  }, []);

  if (!debtData) return <div className="p-8 text-white">Loading debt report...</div>;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h2 className="text-3xl font-extrabold text-white">Technical Debt Analyzer</h2>
        <p className="text-slate-400 mt-1">Code maintainability metrics, long file detection, and refactoring recommendations.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6 flex flex-col justify-between">
          <span className="text-slate-400 font-medium">Overall Debt Penalty Score</span>
          <div className="text-5xl font-extrabold text-amber-400 my-4">{debtData.overall_debt_score} / 100</div>
          <p className="text-xs text-slate-400">Lower is better. Measures accumulation of long functions & missing tests.</p>
        </div>
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6 flex flex-col justify-between">
          <span className="text-slate-400 font-medium">Maintainability Index</span>
          <div className="text-5xl font-extrabold text-emerald-400 my-4">{debtData.overall_maintainability_score}%</div>
          <p className="text-xs text-slate-400">Higher is better. Based on AST complexity metrics.</p>
        </div>
      </div>

      <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6 space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-indigo-400" /> Refactoring Suggestions
        </h3>
        <ul className="space-y-2">
          {debtData.suggestions.map((s: string, idx: number) => (
            <li key={idx} className="p-3 bg-slate-900/60 border border-slate-800 rounded-xl text-sm text-slate-300 flex items-center gap-3">
              <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>{s}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
