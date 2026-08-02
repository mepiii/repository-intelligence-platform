import React, { useState } from 'react';
import { fetchApi } from '../api/client';
import { Search as SearchIcon, Code, FileText } from 'lucide-react';

export const Search: React.FC = () => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('hybrid');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    try {
      const data = await fetchApi(`/search?repo_id=1&q=${encodeURIComponent(query)}&type=${searchType}`);
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-extrabold text-white">Code & Doc Search</h2>
        <p className="text-slate-400 mt-1">Hybrid semantic vector search + keyword matching powered by pgvector.</p>
      </div>

      <form onSubmit={handleSearch} className="flex gap-4">
        <div className="relative flex-1">
          <SearchIcon className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search code, e.g., 'authentication', 'redis cache', 'payment'..."
            className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-12 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>
        <select
          value={searchType}
          onChange={(e) => setSearchType(e.target.value)}
          className="bg-slate-800 border border-slate-700 text-slate-300 px-4 py-3 rounded-xl focus:outline-none focus:border-indigo-500 font-medium"
        >
          <option value="hybrid">Hybrid Search</option>
          <option value="semantic">Semantic Search</option>
          <option value="keyword">Keyword Search</option>
        </select>
        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-6 py-3 rounded-xl transition-all shadow-lg shadow-indigo-600/30"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      <div className="space-y-4">
        {results.map((r, idx) => (
          <div key={idx} className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-indigo-400 font-medium text-sm flex items-center gap-2">
                <Code className="w-4 h-4" /> {r.file_path}
              </span>
              <span className="text-xs font-semibold px-2.5 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 rounded-md">
                Score: {r.score}
              </span>
            </div>
            <pre className="bg-slate-900/90 p-4 rounded-lg text-xs font-mono text-slate-300 overflow-x-auto border border-slate-800">
              {r.content_snippet}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
};
