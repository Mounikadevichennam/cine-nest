import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Play, Info, Star, X } from 'lucide-react';

export default function HeroBanner({ movie }) {
  const [showTrailerModal, setShowTrailerModal] = useState(false);

  if (!movie) return null;

  return (
    <div className="relative w-full h-[75vh] min-h-[500px] max-h-[680px] overflow-hidden bg-[#0B0D12]">
      {/* Background Poster / Backdrop Image */}
      <div className="absolute inset-0">
        <img 
          src={movie.backdrop_url || movie.poster_url} 
          alt={movie.title} 
          className="w-full h-full object-cover object-center opacity-40 scale-102"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#0B0D12] via-[#0B0D12]/50 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-r from-[#0B0D12] via-[#0B0D12]/60 to-transparent" />
      </div>

      {/* Hero Content Overlay */}
      <div className="relative z-20 max-w-7xl mx-auto h-full px-6 flex flex-col justify-end pb-16">
        <div className="max-w-2xl space-y-4">
          {/* Brand & Metadata Badges */}
          <div className="flex items-center space-x-3 text-xs font-semibold">
            <span className="px-2.5 py-1 bg-red-600 text-white rounded text-[11px] font-extrabold uppercase tracking-wider">
              {movie.language}
            </span>
            <span className="text-gray-300 font-bold">{movie.release_year}</span>
            <div className="flex items-center space-x-1 text-amber-400 font-bold">
              <Star className="w-3.5 h-3.5 fill-current" />
              <span>{movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}</span>
            </div>
            <span className="text-gray-400 font-mono text-[11px] uppercase border-l border-gray-700 pl-3">Personalized Pick</span>
          </div>

          {/* Movie Title */}
          <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight leading-none drop-shadow-lg">
            {movie.title}
          </h1>

          {/* Description */}
          <p className="text-sm sm:text-base text-gray-300 line-clamp-3 max-w-xl font-normal leading-relaxed">
            {movie.description || movie.storyline}
          </p>

          {/* Action Buttons */}
          <div className="flex items-center space-x-4 pt-3">
            <Link 
              to={`/watch/${movie.id}`}
              className="px-7 py-3.5 bg-red-600 hover:bg-red-700 text-white font-extrabold text-sm rounded-lg flex items-center space-x-2.5 shadow-xl shadow-red-950/60 transition transform hover:scale-105"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Watch Now</span>
            </Link>

            {movie.trailer_url && (
              <button 
                onClick={() => setShowTrailerModal(true)}
                className="px-6 py-3.5 bg-gray-900/90 hover:bg-gray-800 text-gray-200 font-bold text-sm rounded-lg flex items-center space-x-2 border border-gray-700 transition"
              >
                <Info className="w-4 h-4 text-red-500" />
                <span>Trailer</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Trailer Modal */}
      {showTrailerModal && movie.trailer_url && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="relative w-full max-w-4xl bg-[#141824] rounded-xl overflow-hidden border border-gray-800 shadow-2xl">
            <button 
              onClick={() => setShowTrailerModal(false)}
              className="absolute top-3 right-3 z-50 p-2 bg-black/70 hover:bg-red-600 text-white rounded-full transition"
            >
              <X className="w-5 h-5" />
            </button>
            <div className="aspect-video w-full">
              <iframe 
                src={`${movie.trailer_url}?autoplay=1`} 
                title={`${movie.title} Trailer`}
                className="w-full h-full"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
