import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import MovieCard from '../components/MovieCard';
import { movieService } from '../services/movieService';
import { Search as SearchIcon, X, History } from 'lucide-react';

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    const delayDebounceFn = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await movieService.searchMovies(query);
        setResults(data);
      } catch (err) {
        console.error("Search failed:", err);
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
        {query && (
          <div className="flex items-center justify-between text-xs text-gray-400 pt-2">
            <span>Showing results for "<span className="text-white font-semibold">{query}</span>"</span>
            <span>{results.length} movies found</span>
          </div>
        )}

        {/* Results Grid */}
        {loading ? (
          <div className="py-20 text-center text-gray-400 font-mono text-xs">
            Searching catalog...
          </div>
        ) : results.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6 pt-2">
            {results.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        ) : query ? (
          <div className="py-20 text-center bg-[#141824] rounded-xl border border-gray-800">
            <SearchIcon className="w-10 h-10 text-gray-600 mx-auto mb-3" />
            <p className="text-sm font-semibold text-gray-300">No movies match "{query}"</p>
            <p className="text-xs text-gray-500 mt-1">Try searching for Pushpa, RRR, Kantara, Action, or Telugu.</p>
          </div>
        ) : (
          <div className="py-16 text-center text-gray-500 text-xs">
            Type title, actor name, or genre to begin searching.
          </div>
        )}
      </div>
    </div>
  );
}
