import React, { useRef } from 'react';
import MovieCard from './MovieCard';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function MovieRow({ title, movies = [], icon: Icon }) {
  const rowRef = useRef(null);

  const scroll = (direction) => {
    if (rowRef.current) {
      const { scrollLeft, clientWidth } = rowRef.current;
      const scrollAmount = clientWidth * 0.75;
      rowRef.current.scrollTo({
        left: direction === 'left' ? scrollLeft - scrollAmount : scrollLeft + scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  if (!movies || movies.length === 0) return null;

  return (
    <div className="space-y-3 py-4">
      {/* Row Header */}
      <div className="flex items-center space-x-2 px-6">
        {Icon && <Icon className="w-5 h-5 text-red-500" />}
        <h2 className="text-lg font-extrabold text-white tracking-wide">{title}</h2>
      </div>

      {/* Row Content Carousel */}
      <div className="relative group px-6">
        <button 
          onClick={() => scroll('left')}
          className="absolute left-1 top-1/2 -translate-y-1/2 z-40 w-9 h-12 bg-black/70 hover:bg-red-600 text-white opacity-0 group-hover:opacity-100 transition flex items-center justify-center rounded-r-md backdrop-blur-sm shadow-xl"
        >
          <ChevronLeft className="w-6 h-6" />
        </button>

        <div 
          ref={rowRef}
          className="flex items-center space-x-4 overflow-x-auto no-scrollbar scroll-smooth py-2"
        >
          {movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>

        <button 
          onClick={() => scroll('right')}
          className="absolute right-1 top-1/2 -translate-y-1/2 z-40 w-9 h-12 bg-black/70 hover:bg-red-600 text-white opacity-0 group-hover:opacity-100 transition flex items-center justify-center rounded-l-md backdrop-blur-sm shadow-xl"
        >
          <ChevronRight className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
}
