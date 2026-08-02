import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Overview } from './pages/Overview';
import { Search } from './pages/Search';
import { KnowledgeGraph } from './pages/KnowledgeGraph';
import { Timeline } from './pages/Timeline';
import { TechnicalDebt } from './pages/TechnicalDebt';
import { AIAssistant } from './pages/AIAssistant';
import { Settings } from './pages/Settings';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');

  const renderContent = () => {
    switch (activeTab) {
      case 'overview': return <Overview />;
      case 'search': return <Search />;
      case 'graph': return <KnowledgeGraph />;
      case 'timeline': return <Timeline />;
      case 'debt': return <TechnicalDebt />;
      case 'assistant': return <AIAssistant />;
      case 'settings': return <Settings />;
      default: return <Overview />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="flex-1">{renderContent()}</main>
    </div>
  );
};
