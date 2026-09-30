import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import AdminSidebar from '../../components/admin/AdminSidebar';
import AdminHeader from '../../components/admin/AdminHeader';
import MovieTable from '../../components/admin/MovieTable';
import { adminService } from '../../services/adminService';
import { PlusCircle, Search } from 'lucide-react';

export default function MovieManagement() {
  const [movies, setMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchMovies = async () => {
    setLoading(true);
    try {
      const data = await adminService.getAdminMovies();
      setMovies(data);
    } catch (err) {
      console.error("Failed to fetch admin movies:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovies();
  }, []);

  const handleDelete = async (movieId) => {
    if (window.confirm("Are you sure you want to delete this movie record?")) {
      try {
        await adminService.deleteMovie(movieId);
        setMovies(movies.filter((m) => m.id !== movieId));
      } catch (err) {
        console.error("Failed to delete movie:", err);
      }
    }
  };

  const filteredMovies = movies.filter((m) => 
    m.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    m.language.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex min-h-screen bg-[#0B0D12] text-white">
      <AdminSidebar />
      <div className="flex-1 flex flex-col">
        <AdminHeader title="Movie Catalog Management" />

        <main className="p-8 space-y-6 max-w-7xl">
          {/* Header & Controls */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="relative max-w-md w-full">
              <Search className="absolute left-3.5 top-3 w-4 h-4 text-gray-500" />
              <input 
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search catalog by title or language..."
                className="w-full pl-10 pr-4 py-2 bg-[#141824] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
              />
            </div>

            <Link
              to="/admin/movies/add"
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-lg flex items-center space-x-2 shadow-lg shadow-red-950/40"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Add New Movie</span>
            </Link>
          </div>

          {/* Catalog Table */}
          {loading ? (
            <div className="py-20 text-center text-gray-500 text-xs font-mono">Loading Catalog Table...</div>
          ) : (
            <MovieTable movies={filteredMovies} onDelete={handleDelete} />
          )}
        </main>
      </div>
    </div>
  );
}
