import React, { useState, useEffect } from 'react';
import AdminSidebar from '../../components/admin/AdminSidebar';
import AdminHeader from '../../components/admin/AdminHeader';
import { adminService } from '../../services/adminService';
import { Film, Users, Globe, Clock, PlusCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await adminService.getStats();
        setStats(data);
      } catch (err) {
        console.error("Failed to load admin stats:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#0B0D12] text-white">
      <AdminSidebar />
      <div className="flex-1 flex flex-col">
        <AdminHeader title="Admin Dashboard" />

        <main className="p-8 space-y-8 max-w-7xl">
          {/* Quick Action Bar */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-black">System Overview</h2>
              <p className="text-xs text-gray-400">Real-time catalog metrics and subscriber analytics</p>
            </div>
            <Link
              to="/admin/movies/add"
              className="px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-lg flex items-center space-x-2 shadow-lg shadow-red-950/40"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Add New Movie</span>
            </Link>
          </div>

          {/* Stats Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-[#141824] p-6 rounded-2xl border border-gray-800 space-y-2">
              <div className="flex items-center justify-between text-gray-400">
                <span className="text-xs font-semibold uppercase tracking-wider">Total Catalog Movies</span>
                <Film className="w-5 h-5 text-red-500" />
              </div>
              <p className="text-3xl font-black text-white">{stats ? stats.total_movies : '--'}</p>
            </div>

            <div className="bg-[#141824] p-6 rounded-2xl border border-gray-800 space-y-2">
              <div className="flex items-center justify-between text-gray-400">
                <span className="text-xs font-semibold uppercase tracking-wider">Subscribers</span>
                <Users className="w-5 h-5 text-blue-500" />
              </div>
              <p className="text-3xl font-black text-white">{stats ? stats.total_users : '--'}</p>
            </div>

            <div className="bg-[#141824] p-6 rounded-2xl border border-gray-800 space-y-2">
              <div className="flex items-center justify-between text-gray-400">
                <span className="text-xs font-semibold uppercase tracking-wider">Popular Language</span>
                <Globe className="w-5 h-5 text-teal-500" />
              </div>
              <p className="text-3xl font-black text-white">{stats ? stats.popular_language : 'Telugu'}</p>
            </div>

            <div className="bg-[#141824] p-6 rounded-2xl border border-gray-800 space-y-2">
              <div className="flex items-center justify-between text-gray-400">
                <span className="text-xs font-semibold uppercase tracking-wider">Stream Watch Hours</span>
                <Clock className="w-5 h-5 text-amber-500" />
              </div>
              <p className="text-3xl font-black text-white">{stats ? `${stats.total_watch_hours} hrs` : '--'}</p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
