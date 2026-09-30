import React from 'react';
import { Link } from 'react-router-dom';
import { Edit2, Trash2, Star, ExternalLink } from 'lucide-react';

export default function MovieTable({ movies, onDelete }) {
  if (!movies || movies.length === 0) {
    return (
      <div className="py-12 text-center text-gray-500 text-xs bg-[#141824] rounded-xl border border-gray-800">
        No movies currently in catalog. Use "Add Movie" to insert new records.
      </div>
    );
  }

  return (
    <div className="bg-[#141824] rounded-xl border border-gray-800 overflow-hidden shadow-xl">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-gray-300">
          <thead className="bg-[#0B0D12] text-gray-400 font-bold uppercase tracking-wider border-b border-gray-800">
            <tr>
              <th className="px-6 py-4">Movie</th>
              <th className="px-6 py-4">Language</th>
              <th className="px-6 py-4">Release Year</th>
              <th className="px-6 py-4">Rating</th>
              <th className="px-6 py-4">Trailer</th>
              <th className="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {movies.map((movie) => (
              <tr key={movie.id} className="hover:bg-gray-800/40 transition">
                <td className="px-6 py-3 flex items-center space-x-3">
                  <img src={movie.poster_url} alt={movie.title} className="w-10 h-14 object-cover rounded border border-gray-700" />
                  <div>
                    <p className="font-bold text-white text-sm">{movie.title}</p>
                    <p className="text-[10px] text-gray-500">ID: {movie.id} | IMDb: {movie.imdb_id || 'N/A'}</p>
                  </div>
                </td>
                <td className="px-6 py-3">
                  <span className="px-2.5 py-0.5 bg-gray-800 text-gray-200 rounded font-semibold text-[10px]">
                    {movie.language}
                  </span>
                </td>
                <td className="px-6 py-3 font-medium">{movie.release_year}</td>
                <td className="px-6 py-3">
                  <div className="flex items-center space-x-1 text-amber-400 font-bold">
                    <Star className="w-3.5 h-3.5 fill-current" />
                    <span>{movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}</span>
                  </div>
                </td>
                <td className="px-6 py-3">
                  {movie.trailer_url ? (
                    <a href={movie.trailer_url} target="_blank" rel="noreferrer" className="text-red-500 hover:underline flex items-center space-x-1">
                      <span>Available</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  ) : <span className="text-gray-600">None</span>}
                </td>
                <td className="px-6 py-3 text-right">
                  <div className="flex items-center justify-end space-x-3">
                    <Link to={`/admin/movies/edit/${movie.id}`} className="text-blue-400 hover:text-blue-300 p-1">
                      <Edit2 className="w-4 h-4" />
                    </Link>
                    <button onClick={() => onDelete(movie.id)} className="text-red-500 hover:text-red-400 p-1">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
