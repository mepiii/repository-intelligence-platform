import React from 'react';
import { Terminal, Search, GitGraph, Clock, AlertTriangle, Bot, Settings as SettingsIcon } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: Terminal },
    { id: 'search', label: 'Search', icon: Search },
    { id: 'graph', label: 'Knowledge Graph', icon: GitGraph },
    { id: 'timeline', label: 'Timeline', icon: Clock },
    { id: 'debt', label: 'Technical Debt', icon: AlertTriangle },
    { id: 'assistant', label: 'AI Assistant', icon: Bot },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  return (
    <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="p-2 bg-indigo-600 rounded-lg text-white font-bold text-xl">
          RI
        </div>
        <div>
          <h1 className="text-lg font-bold text-slate-100">Repository Intelligence</h1>
          <p className="text-xs text-slate-400">Production v1.0 • Early Sourcegraph AI</p>
        </div>
      </div>
      <nav className="flex space-x-1 bg-slate-900/50 p-1.5 rounded-xl border border-slate-700/50">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </header>
  );
};
