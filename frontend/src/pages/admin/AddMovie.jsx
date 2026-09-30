import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdminSidebar from '../../components/admin/AdminSidebar';
import AdminHeader from '../../components/admin/AdminHeader';
import MovieForm from '../../components/admin/MovieForm';
import { adminService } from '../../services/adminService';

export default function AddMovie() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (moviePayload) => {
    setLoading(true);
    try {
      await adminService.createMovie(moviePayload);
      navigate('/admin/movies');
    } catch (err) {
      console.error("Failed to create movie:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0B0D12] text-white">
      <AdminSidebar />
      <div className="flex-1 flex flex-col">
        <AdminHeader title="Add New Movie Record" />

        <main className="p-8 max-w-4xl space-y-6">
          <p className="text-xs text-gray-400">Add metadata, poster URL, optional trailer, genres, and cast to the catalog database.</p>
          <MovieForm onSubmit={handleSubmit} loading={loading} />
        </main>
      </div>
    </div>
  );
}
