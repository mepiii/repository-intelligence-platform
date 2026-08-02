import React, { useEffect, useState } from 'react';
import { fetchApi } from '../api/client';
import { GitGraph, Database, Code, Shield } from 'lucide-react';

export const KnowledgeGraph: React.FC = () => {
  const [graph, setGraph] = useState<{ nodes: any[]; edges: any[] }>({ nodes: [], edges: [] });

  useEffect(() => {
    fetchApi('/graph?repo_id=1')
      .then(data => setGraph(data))
      .catch(console.error);
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-extrabold text-white">Repository Knowledge Graph</h2>
        <p className="text-slate-400 mt-1">Neo4j graph entity topology connecting Files, Functions, Classes, and Commits.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6 min-h-[450px] flex flex-col items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#6366f1_1px,transparent_1px)] [background-size:16px_16px]"></div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 z-10 w-full">
            {graph.nodes.slice(0, 9).map((node, i) => (
              <div key={i} className="p-4 bg-slate-900/90 border border-indigo-500/30 rounded-xl shadow-lg flex flex-col items-center text-center space-y-2">
                <div className="p-2 bg-indigo-600/20 rounded-lg text-indigo-400">
                  <GitGraph className="w-5 h-5" />
                </div>
                <span className="text-xs font-bold text-slate-200 truncate w-full">{node.name}</span>
                <span className="text-[10px] px-2 py-0.5 bg-slate-800 text-indigo-300 rounded font-mono uppercase">
                  {node.label}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl p-6 space-y-4">
          <h3 className="text-lg font-bold text-white">Graph Topology Summary</h3>
          <div className="space-y-3">
            <div className="flex justify-between p-3 bg-slate-900/60 rounded-xl">
              <span className="text-sm text-slate-400">Total Nodes</span>
              <span className="font-bold text-indigo-400">{graph.nodes.length}</span>
            </div>
            <div className="flex justify-between p-3 bg-slate-900/60 rounded-xl">
              <span className="text-sm text-slate-400 font-medium">Total Relationships</span>
              <span className="font-bold text-cyan-400">{graph.edges.length}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
