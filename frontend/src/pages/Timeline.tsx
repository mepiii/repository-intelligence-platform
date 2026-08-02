import React, { useEffect, useState } from 'react';
import { fetchApi } from '../api/client';
import { GitCommit, Tag, Package, Wrench } from 'lucide-react';

export const Timeline: React.FC = () => {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    fetchApi('/timeline?repo_id=1')
      .then(data => setEvents(data))
      .catch(console.error);
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-extrabold text-white">Repository Timeline</h2>
        <p className="text-slate-400 mt-1">Chronological history of commits, releases, dependency additions, and refactors.</p>
      </div>

      <div className="relative border-l-2 border-slate-700 ml-4 space-y-6 pl-6">
        {events.map((ev, idx) => (
          <div key={idx} className="relative group">
            <div className="absolute -left-[31px] top-1 p-1.5 bg-slate-900 border border-slate-700 rounded-full text-indigo-400">
              <GitCommit className="w-4 h-4" />
            </div>
            <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 space-y-1">
              <div className="flex justify-between items-center text-xs text-slate-400 font-mono">
                <span className="uppercase font-bold text-indigo-400">{ev.event_type}</span>
                <span>{new Date(ev.timestamp).toLocaleString()}</span>
              </div>
              <p className="text-slate-200 text-sm font-medium">{ev.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
