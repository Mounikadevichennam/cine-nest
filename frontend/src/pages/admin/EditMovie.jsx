import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AdminSidebar from '../../components/admin/AdminSidebar';
import AdminHeader from '../../components/admin/AdminHeader';
import MovieForm from '../../components/admin/MovieForm';
import { adminService } from '../../services/adminService';
import { movieService } from '../../services/movieService';

export default function EditMovie() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const data = await movieService.getMovieDetails(id);
        setMovie(data);
      } catch (err) {
        console.error("Failed to load movie for edit:", err);
      }
    };
    fetchMovie();
  }, [id]);

  const handleSubmit = async (moviePayload) => {
    setLoading(true);
    try {
      await adminService.updateMovie(id, moviePayload);
      navigate('/admin/movies');
    } catch (err) {
      console.error("Failed to update movie:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0B0D12] text-white">
      <AdminSidebar />
      <div className="flex-1 flex flex-col">
        <AdminHeader title="Edit Movie Record" />

        <main className="p-8 max-w-4xl space-y-6">
          <p className="text-xs text-gray-400">Update catalog metadata, poster URL, optional trailer, genres, and storyline for ID #{id}.</p>
          {movie ? (
            <MovieForm initialData={movie} onSubmit={handleSubmit} loading={loading} />
          ) : (
            <div className="text-xs text-gray-500 font-mono">Loading Movie Record...</div>
          )}
        </main>
      </div>
    </div>
  );
}
