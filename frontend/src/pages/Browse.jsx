import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import MovieCard from '../components/MovieCard';
import { movieService } from '../services/movieService';
import { SlidersHorizontal, Filter, RefreshCw } from 'lucide-react';

const LANGUAGES = ["All", "Telugu", "Hindi", "Tamil", "Malayalam", "Kannada", "English", "Korean", "Japanese", "Spanish", "French", "Chinese"];
const GENRES = ["All", "Action", "Comedy", "Drama", "Crime", "Thriller", "Sci-Fi", "Romance", "Adventure", "Horror", "History", "Fantasy", "Mystery"];
const YEARS = ["All", 2026, 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016];

export default function Browse() {
  const [movies, setMovies] = useState([]);
  const [language, setLanguage] = useState("All");
  const [genre, setGenre] = useState("All");
  const [year, setYear] = useState("All");
  const [minRating, setMinRating] = useState(0);
  const [loading, setLoading] = useState(true);

  const fetchMovies = async () => {
    setLoading(true);
    try {
      const params = {};
      if (language !== "All") params.language = language;
      if (genre !== "All") params.genre = genre;
      if (year !== "All") params.year = year;
      if (minRating > 0) params.min_rating = minRating;

      const data = await movieService.getMovies(params);
      setMovies(data);
    } catch (err) {
      console.error("Failed to browse movies:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovies();
  }, [language, genre, year, minRating]);

  const resetFilters = () => {
    setLanguage("All");
    setGenre("All");
    setYear("All");
    setMinRating(0);
  };

  return (
    <div className="min-h-screen bg-[#0B0D12] text-white pt-24 pb-20">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 space-y-6">
        {/* Header & Filter Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-gray-800">
          <div>
            <h1 className="text-3xl font-extrabold flex items-center space-x-2">
              <Filter className="w-6 h-6 text-red-500" />
              <span>Browse Catalog</span>
            </h1>
            <p className="text-xs text-gray-400 mt-1">Filter regional movies by language, genre, year, or rating</p>
          </div>

          <button 
            onClick={resetFilters}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs font-semibold rounded-lg transition self-start md:self-auto"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset Filters</span>
          </button>
        </div>

        {/* Filter Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 bg-[#141824] p-4 rounded-xl border border-gray-800/80 shadow-lg">
          {/* Language Filter */}
          <div>
            <label className="block text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Language</label>
            <select 
              value={language} 
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full bg-[#0B0D12] border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-red-500"
            >
              {LANGUAGES.map((lang) => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>

          {/* Genre Filter */}
          <div>
            <label className="block text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Genre</label>
            <select 
              value={genre} 
              onChange={(e) => setGenre(e.target.value)}
              className="w-full bg-[#0B0D12] border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-red-500"
            >
              {GENRES.map((g) => (
                <option key={g} value={g}>{g}</option>
              ))}
            </select>
          </div>

          {/* Year Filter */}
          <div>
            <label className="block text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Release Year</label>
            <select 
              value={year} 
              onChange={(e) => setYear(e.target.value)}
              className="w-full bg-[#0B0D12] border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-red-500"
            >
              {YEARS.map((y) => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>

          {/* Rating Filter */}
          <div>
            <label className="block text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Min IMDb/TMDB Rating</label>
            <select 
              value={minRating} 
              onChange={(e) => setMinRating(parseFloat(e.target.value))}
              className="w-full bg-[#0B0D12] border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-red-500"
            >
              <option value={0}>Any Rating</option>
              <option value={8}>8.0+ Stars</option>
              <option value={7}>7.0+ Stars</option>
              <option value={6}>6.0+ Stars</option>
            </select>
          </div>
        </div>

        {/* Movies Responsive Grid */}
        {loading ? (
          <div className="py-20 text-center text-gray-400 font-mono text-xs">
            Loading Catalog Movies...
          </div>
        ) : movies.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6 pt-4">
            {movies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        ) : (
          <div className="py-20 text-center bg-[#141824] rounded-xl border border-gray-800">
            <SlidersHorizontal className="w-10 h-10 text-gray-600 mx-auto mb-3" />
            <p className="text-sm font-semibold text-gray-300">No movies found for selected filters</p>
            <p className="text-xs text-gray-500 mt-1">Try resetting filters to see more regional titles.</p>
          </div>
        )}
      </div>
    </div>
  );
}
