import React, { useState } from 'react';
import { fetchApi } from '../api/client';
import { Bot, Send, Sparkles, BookOpen } from 'lucide-react';

export const AIAssistant: React.FC = () => {
  const [messages, setMessages] = useState<any[]>([
    {
      sender: 'ai',
      text: 'Hello! I am your AI Repository Assistant. Ask me anything about authentication, caching, payment logic, or technical debt!',
      citations: [],
      reasoning: []
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const samplePrompts = [
    "Explain authentication system.",
    "Why was Redis introduced?",
    "Where is payment implemented?",
    "Which modules are technical debt?"
  ];

  const handleSend = async (queryText?: string) => {
    const promptToUse = queryText || input;
    if (!promptToUse.trim()) return;

    const userMsg = { sender: 'user', text: promptToUse };
    setMessages(prev => [...prev, userMsg]);
    if (!queryText) setInput('');
    setLoading(true);

    try {
      const res = await fetchApi('/assistant/chat', {
        method: 'POST',
        body: JSON.stringify({ repo_id: 1, message: promptToUse })
      });

      setMessages(prev => [
        ...prev,
        {
          sender: 'ai',
          text: res.answer,
          citations: res.citations,
          reasoning: res.reasoning_steps
        }
      ]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6 flex flex-col h-[calc(100vh-120px)]">
      <div>
        <h2 className="text-3xl font-extrabold text-white flex items-center gap-3">
          <Bot className="w-8 h-8 text-indigo-400" /> AI Repository Assistant
        </h2>
        <p className="text-slate-400 mt-1">Multi-source RAG synthesizing code AST, pgvector search, and Neo4j graph context.</p>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        {samplePrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(p)}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-xs text-indigo-300 font-medium whitespace-nowrap transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 inline mr-1 text-indigo-400" /> {p}
          </button>
        ))}
      </div>

      <div className="flex-1 bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 overflow-y-auto space-y-4">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
            <div
              className={`max-w-2xl p-4 rounded-2xl text-sm leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-indigo-600 text-white font-medium'
                  : 'bg-slate-900/90 text-slate-200 border border-slate-700/60'
              }`}
            >
              <div className="whitespace-pre-wrap">{m.text}</div>
              
              {m.citations && m.citations.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-800 space-y-1">
                  <span className="text-xs font-bold text-indigo-400 flex items-center gap-1">
                    <BookOpen className="w-3.5 h-3.5" /> Repository Citations:
                  </span>
                  {m.citations.map((c: any, ci: number) => (
                    <div key={ci} className="text-xs text-slate-400 font-mono">
                      • {c.file_path} (Relevance: {c.score})
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about the repository..."
          className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-medium flex items-center gap-2 transition-all shadow-lg shadow-indigo-600/30"
        >
          <Send className="w-4 h-4" /> {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  );
};
