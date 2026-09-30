import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Star, Play, Film } from 'lucide-react';

export default function MovieCard({ movie }) {
  const getInitialPoster = (m) => {
    if (!m) return null;
    if (m.poster_url && m.poster_url.startsWith('http')) {
      return m.poster_url;
    }
    if (m.poster_path) {
      return `https://image.tmdb.org/t/p/w500${m.poster_path}`;
    }
    return null;
  };

  const [imgSrc, setImgSrc] = useState(() => getInitialPoster(movie));
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    setImgSrc(getInitialPoster(movie));
    setHasError(false);
  }, [movie]);

  if (!movie) return null;

  return (
    <div className="group relative flex-shrink-0 w-40 sm:w-48 bg-[#141824] rounded-lg overflow-hidden border border-gray-800/80 hover:border-red-600/60 shadow-lg hover:shadow-red-950/20 transition-all duration-300 transform hover:-translate-y-1">
      <Link to={`/movie/${movie.id}`}>
        {/* Poster Image Container */}
        <div className="relative aspect-[2/3] w-full overflow-hidden bg-gray-900 flex items-center justify-center">
          {!hasError && imgSrc ? (
            <img 
              src={imgSrc} 
              alt={movie.title} 
              onError={() => setHasError(true)}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-[#1c2234] to-[#0d1019] p-4 flex flex-col justify-between text-center border border-gray-800">
              <Film className="w-8 h-8 text-red-600/70 mx-auto mt-4" />
              <div>
                <p className="text-xs font-black text-white line-clamp-2 uppercase tracking-wider">{movie.title}</p>
                <p className="text-[10px] text-gray-400 mt-1">{movie.release_year}</p>
              </div>
              <span className="text-[9px] font-bold text-red-500 uppercase tracking-widest pb-1">CineNest</span>
            </div>
          )}

          {/* Overlay Play Icon on Hover */}
          <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
            <div className="w-11 h-11 rounded-full bg-red-600 flex items-center justify-center text-white shadow-lg transform group-hover:scale-110 transition-transform">
              <Play className="w-5 h-5 fill-current ml-0.5" />
            </div>
          </div>

          {/* Language Tag */}
          <span className="absolute top-2 left-2 px-2 py-0.5 bg-black/75 backdrop-blur-sm text-[10px] font-bold tracking-wider text-gray-200 uppercase rounded border border-white/10">
            {movie.language}
          </span>
        </div>

        {/* Info Box */}
        <div className="p-3">
          <h3 className="text-xs font-bold text-white truncate group-hover:text-red-500 transition-colors">
            {movie.title}
          </h3>
          <div className="flex items-center justify-between mt-1.5 text-[11px] text-gray-400">
            <span>{movie.release_year}</span>
            <div className="flex items-center space-x-1 text-amber-400 font-semibold">
              <Star className="w-3 h-3 fill-current" />
              <span>{movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}</span>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );
}
