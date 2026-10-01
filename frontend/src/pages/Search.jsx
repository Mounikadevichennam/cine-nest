import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import MovieCard from '../components/MovieCard';
import { movieService } from '../services/movieService';
import { Search as SearchIcon, X, AlertCircle } from 'lucide-react';

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setError(null);
      return;
    }

    const delayDebounceFn = setTimeout(async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await movieService.searchMovies(query);
        setResults(data || []);
      } catch (err) {
        console.error("Search failed:", err);
        setError("Search request failed. Please check backend connection.");
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  return (
    <div className="min-h-screen bg-[#0B0D12] text-white pt-24 pb-20">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 space-y-6">
        {/* Search Input Bar */}
        <div className="relative max-w-3xl mx-auto">
          <SearchIcon className="absolute left-4 top-4 w-6 h-6 text-gray-400" />
          <input 
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by movie title, actor, genre, or language..."
            className="w-full pl-14 pr-12 py-3.5 bg-[#141824] border border-gray-700 focus:border-red-500 rounded-xl text-base text-white focus:outline-none shadow-xl transition"
          />
          {query && (
            <button 
              onClick={() => setQuery('')}
              className="absolute right-4 top-4 p-1 hover:bg-gray-800 rounded-full text-gray-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Results Header */}
        {query && !loading && !error && (
          <div className="flex items-center justify-between text-xs text-gray-400 pt-2">
            <span>Showing results for "<span className="text-white font-semibold">{query}</span>"</span>
            <span>{results.length} movies found</span>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="p-4 bg-red-950/60 border border-red-800 text-red-300 text-xs rounded-xl flex items-center justify-center space-x-2 max-w-2xl mx-auto">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Results Grid */}
        {loading ? (
          <div className="py-20 text-center text-gray-400 font-mono text-sm">
            Loading movies...
          </div>
        ) : results.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6 pt-2">
            {results.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        ) : query ? (
          <div className="py-20 text-center bg-[#141824] rounded-xl border border-gray-800 max-w-2xl mx-auto">
            <SearchIcon className="w-10 h-10 text-gray-600 mx-auto mb-3" />
            <p className="text-base font-semibold text-gray-300">No movies found</p>
            <p className="text-xs text-gray-500 mt-1">Try searching for RRR, Pawan Kalyan, Prabhas, Action, or 2025.</p>
          </div>
        ) : (
          <div className="py-16 text-center text-gray-500 text-xs">
            Type movie title, actor name, genre, language, or year to begin searching.
          </div>
        )}
      </div>
    </div>
  );
}
